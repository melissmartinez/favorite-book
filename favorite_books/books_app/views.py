from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt



def index(request):
    if request.method == "GET":
        if request.session.__contains__('userid'):
            return redirect('/books')
        else:
            context = {
            }
            return render(request, 'index.html', context)
    if request.method == "POST":
        if request.POST['reg_or_log'] == "reg":
            errors = User.objects.basic_validator(request.POST)
            if len(errors) > 0:
                for k, v in errors.items():
                    messages.error(request, v, extra_tags='register')
                print(messages.get_messages(request))
                return redirect('/')
            else: 
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                print(pw_hash)
                user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
                request.session['userid'] = user.id
                messages.success(request, "Successfuly registered (or logged in)!")
                return redirect('/books')
        if request.POST['reg_or_log'] == "log":
            user = User.objects.filter(email=request.POST['email'])
            if user:
                logged_user=user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                    messages.success(request, "Successfuly registered (or logged in)!")
                    return redirect('/books')
            messages.error(request, "Invalid email or password", extra_tags="login")
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def books(request):
    if request.method == 'GET':
        if not request.session['userid']:
            return redirect('/')
        context = {
            'user': User.objects.get(id=request.session['userid']),
            "books": Book.objects.all()
        }
        return render(request, 'books.html', context)
    if request.method == 'POST':
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/books')
        else: 
            user = User.objects.get(id=request.session['userid'])
            book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], creator=user)
            book.favorites.add(user)
            return redirect('/books')

def show(request, book_id):
    if request.method == 'GET':
        if not request.session['userid']:
            return redirect('/')
        context = {
            'user': User.objects.get(id=request.session['userid']),
            'book': Book.objects.get(id=book_id)
        }
        return render(request, 'show.html', context)
    if request.method == 'POST':
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            book = Book.objects.get(id=request.POST['book_id'])
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/books/{book.id}')
        else:
            book = Book.objects.get(id=request.POST['book_id'])
            book.title = request.POST['title']
            book.desc = request.POST['desc']
            book.save()
        return redirect(f'/books/{book.id}')

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session['userid'])
    book = Book.objects.get(id=book_id)
    user.favorites.add(book)
    return redirect(f"/books/{book.id}")

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session['userid'])
    book = Book.objects.get(id=book_id)
    user.favorites.remove(book)
    return redirect("/books")