from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from django.shortcuts import redirect
from django.templatetags.static import static
import re
from functools import wraps
import random
import os

def add_random_media(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if random.choice(['image'] * 9 + ['video']) == 'image':
            media_dir = os.path.join(settings.BASE_DIR, 'vulnerable_app', 'static', 'images')
            media_type = 'image'
        else:
            media_dir = os.path.join(settings.BASE_DIR, 'vulnerable_app', 'static', 'videos')
            media_type = 'video'

        media_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
        media_name = random.choice(media_files) if media_files else None
        response = view_func(request, *args, **kwargs, media_type=media_type, media_name=media_name)
        return response
    return wrapper


def redirect_to_admin1(request):
    return redirect('admin1')


# can do anything
# one solution: admin' --
@add_random_media
def admin1(request, media_type=None, media_name=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            query = f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return render(request, 'vulnerable_app/login_success.html', {'media_type': media_type, 'media_name': media_name})
        else:
            return render(request, 'vulnerable_app/login_fail.html')

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 1'})


# Note: can paramaterize to mitigate vulnerability:
# cursor.execute("SELECT * FROM vulnerable_app_user WHERE username = %s AND password = %s", [username, password])
# or can use Django ORM
# user = User.objects.filter(username=username, password=password).first()
# or import authenticate: from django.contrib.auth import authenticate, login

# No comments
# One solution (put for both username and password): ' OR '1'='1
@add_random_media
def admin2(request, media_type=None, media_name=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        username = username.replace("-", "")
        password = password.replace("-", "")

        with connection.cursor() as cursor:
            query = f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return render(request, 'vulnerable_app/login_success.html', {'media_type': media_type, 'media_name': media_name})
        else:
            return render(request, 'vulnerable_app/login_fail.html')

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 2'})
