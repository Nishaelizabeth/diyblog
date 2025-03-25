from django.contrib import admin
from .models import Blog, BlogAuthor, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'content')
    inlines = [CommentInline]

@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'blog', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('description', 'author__username')
