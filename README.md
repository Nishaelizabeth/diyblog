# DIY Blog

A modern blog application built with Django that allows users to create, read, comment on, and like blog posts.

## Features

- User authentication (login, register, logout)
- Create and manage blog posts
- Comment on blog posts
- Like/unlike blog posts
- User profiles with bio
- Search functionality
- Responsive design using Bootstrap
- Modern UI with Font Awesome icons

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mini_blog_nisha
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to see the application.

## Usage

1. Register a new account or login with existing credentials
2. Create blog posts through the admin interface
3. View all blog posts on the home page
4. Click on a blog post to view details and add comments
5. Like/unlike posts
6. Update your profile with bio information
7. Search for blog posts using the search bar

## License

This project is licensed under the MIT License.
