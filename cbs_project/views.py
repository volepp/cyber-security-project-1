from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import sqlite3

from .models import Book
from .forms import UserForm

def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    return redirect("/login")
    
@login_required
# FLAW 2: CSRF exempted
# Fix: remove the row below and apply the fix in index.html row 41
@csrf_exempt
def add_book(request):
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        book = Book(reader=request.user, book_name=book_name, read=False)
        book.save()

        return redirect("/")

@login_required
def read_book(request):
    set_book_read(request, True)
    return redirect("/")


@login_required
def unread_book(request):
    set_book_read(request, False)
    return redirect("/")


def set_book_read(request, read):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        book = Book.objects.get(pk=book_id)

        # FLAW 4: Broken access control: 
        # no check whether the user is the book's reader
        #
        # Fix:
        # if book.reader != request.user:
        #     return redirect("/")

        book.read = read
        book.save()

        return redirect("/")

@login_required
def search(request):
    if request.method == "GET":
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        # FLAW 1: SQL injection
        # For example with query "' and 1==0 UNION SELECT 0, username || " " || password, 0 FROM auth_user;--" you can see other users and their passwords
        response = cursor.execute("SELECT id, book_name, read FROM cbs_project_book WHERE reader_id='%s' AND book_name LIKE '%%%s%%'" % (request.user.id, request.GET.get("searched_book"))).fetchall()
        readlist_books = [Book(id=x[0], book_name=x[1]) for x in filter(lambda x: x[2] == False, response)]
        read_books = [Book(id=x[0], book_name=x[1]) for x in filter(lambda x: x[2] == True, response)]

        return render(request, "pages/index.html", {"readlist_books": readlist_books, "read_books": read_books})

@login_required
def index(request):
    readlist_books = request.user.book_set.exclude(read=True)
    read_books = request.user.book_set.exclude(read=False)

    return render(request, "pages/index.html", {"readlist_books": readlist_books, "read_books": read_books})
