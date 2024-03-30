from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.db import connection
import html
import re

# basic one, can do anything
def admin1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM vulnerable_app_user WHERE username = '{username}' AND password = '{password}'")
            user = cursor.fetchone()

        if user:
            return HttpResponse("Welcome, Admin!")
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 1'})

# Note: can paramaterize to mitigate vulnerability:
# cursor.execute("SELECT * FROM vulnerable_app_user WHERE username = %s AND password = %s", [username, password])
# or can use Django ORM
# user = User.objects.filter(username=username, password=password).first()

# No '
# solution: admin --
def admin2(request):
    if request.method == 'POST':
        username = username.replace("'", "")
        password = password.replace("'", "")

        with connection.cursor() as cursor:
            query = f"SELECT * FROM vulnerable_app_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return HttpResponse("Welcome, Admin!")
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 2'})

# filter many things (but not OR or =)
def admin3(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Filter out ', ", ;, -, and other keywords except for OR and 1=1
        username = re.sub(r'[\'";-]|AND|SELECT|WHERE|FROM|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION| --', '', username, flags=re.IGNORECASE)
        password = re.sub(r'[\'";-]|AND|SELECT|WHERE|FROM|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION| --', '', password, flags=re.IGNORECASE)

        with connection.cursor() as cursor:
            query = f"SELECT * FROM vulnerable_app_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return HttpResponse("Welcome, Admin!")
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 3'})

# $$ to delimit a string instead of single quotes.
# solution: admin$$) OR true OR ($$dummy
def admin4(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        username = re.sub(r'[\'";-]|AND|SELECT|WHERE|FROM|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|--', '', username, flags=re.IGNORECASE)
        password = re.sub(r'[\'";-]|AND|SELECT|WHERE|FROM|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|--', '', password, flags=re.IGNORECASE)

        with connection.cursor() as cursor:
            query = f"SELECT * FROM vulnerable_app_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

        if user:
            return HttpResponse("Welcome, Admin!")
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, 'vulnerable_app/admin.html', {'level': 'Admin 4'})