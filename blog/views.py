from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Blog, BlogAuthor, Comment
from .forms import CommentForm, UserUpdateForm, BlogAuthorUpdateForm, UserRegisterForm, BlogPostForm

# Create your views here.

def index(request):
    """View function for home page of site."""
    num_blogs = Blog.objects.all().count()
    num_authors = BlogAuthor.objects.all().count()
    
    return render(request, 'index.html', {
        'num_blogs': num_blogs,
        'num_authors': num_authors,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            BlogAuthor.objects.create(user=user, bio='')
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            # Get or create BlogAuthor for the current user
            author, created = BlogAuthor.objects.get_or_create(
                user=request.user,
                defaults={'bio': ''}
            )
            blog.author = author
            blog.save()
            messages.success(request, 'Your blog post has been published!')
            return redirect('blog-detail', pk=blog.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_create.html', {'form': form})

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Blog.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__user__username__icontains=query)
            ).order_by('-post_date')
        return Blog.objects.all().order_by('-post_date')

class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class BloggerListView(generic.ListView):
    model = BlogAuthor
    template_name = 'blog/blogger_list.html'

class BloggerDetailView(generic.DetailView):
    model = BlogAuthor
    template_name = 'blog/blogger_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(author=self.object).order_by('-post_date')
        return context

@login_required
def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog-detail', pk=pk)
    return redirect('blog-detail', pk=pk)

@login_required
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return JsonResponse({'likes_count': blog.total_likes()})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            author = request.user.blogauthor
            b_form = BlogAuthorUpdateForm(request.POST, instance=author)
        except BlogAuthor.DoesNotExist:
            b_form = BlogAuthorUpdateForm(request.POST)

        if u_form.is_valid() and b_form.is_valid():
            u_form.save()
            author = b_form.save(commit=False)
            if not hasattr(request.user, 'blogauthor'):
                author.user = request.user
            author.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            author = request.user.blogauthor
            b_form = BlogAuthorUpdateForm(instance=author)
        except BlogAuthor.DoesNotExist:
            b_form = BlogAuthorUpdateForm()

    context = {
        'u_form': u_form,
        'b_form': b_form
    }
    return render(request, 'blog/profile.html', context)
