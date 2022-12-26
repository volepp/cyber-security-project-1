from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# FLAW 5: Broken authentication
# Fix: Uncomment the line below
# from django.contrib.auth.password_validation import validate_password

import sqlite3

from .models import Book
from .forms import UserForm

def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # FLAW 5: Broken authentication
            # Fix: Uncomment the lines below
            # if validate_password(user.password) is not None:
            #     return redirect("/login")
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    return redirect("/login")
    
@login_required
# FLAW 2: CSRF
# Fix: remove the row below and apply the fix in index.html row 46
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
        # Fix: check that the current user is the reader
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
        # Fix 1: use a parameterized query
        # response = cursor.execute("SELECT id, book_name, read FROM cbs_project_book WHERE reader_id=? AND book_name LIKE ?", (request.user.id, "%"+request.GET.get("searched_book")+"%")).fetchall()
        # Fix 2: use the model's filter function. Lines 72 and 73 could be removed in this case.
        # books = Book.objects.filter(book_name__contains=request.GET.get("searched_book"))
        response = cursor.execute("SELECT id, book_name, read FROM cbs_project_book WHERE reader_id='%s' AND book_name LIKE '%%%s%%'" % (request.user.id, request.GET.get("searched_book"))).fetchall()
        
        # Fix 2: additionally, use these uncommented lines instead of the ones below them.
        # readlist_books = [Book(id=x.id, book_name=x.book_name) for x in filter(lambda x: x.read == False, books)]
        # read_books = [Book(id=x.id, book_name=x.book_name) for x in filter(lambda x: x.read == True, books)]
        readlist_books = [Book(id=x[0], book_name=x[1]) for x in filter(lambda x: x[2] == False, response)]
        read_books = [Book(id=x[0], book_name=x[1]) for x in filter(lambda x: x[2] == True, response)]

        return render(request, "pages/index.html", {"readlist_books": readlist_books, "read_books": read_books})

@login_required
def index(request):
    readlist_books = request.user.book_set.exclude(read=True)
    read_books = request.user.book_set.exclude(read=False)

    return render(request, "pages/index.html", {"readlist_books": readlist_books, "read_books": read_books})
