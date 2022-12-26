# CBS Project 1

## Installation

You can install the required dependencies using `pip install -r requirements.txt` either globally or in a virtual environment if you choose to create one with e.g. [venv](https://docs.python.org/3/library/venv.html).

## Flaws

**FLAW 1: SQL injection**

Line: views.py lin 74

The application currently allows the user to perform a successful SQL injection attack with the search field. By using the sqlite3 cursor and forming the SQL query manually in the code without using a parameterized query, it's possible to input a malicious text such as `' and 1==0 UNION SELECT 0, username || " " || password, 0 FROM auth_user;--` which would fetch all the usernames and passwords from the database.

To fix this, a parameterized query could be used. By using the currently commented line 76 instead of line 79, the malicious input won't work anymore. Another way would be to just use the model's filter function. Then you wouldn't have to use the sqlite3 library directly at all. To apply this fix, uncomment the lines 78 and 82-83 in views.py and use those instead of the ones that are currently in use (lines 79 and 84-85). 

**FLAW 2: CSRF**

Line: views.py line 29, index.html line 46

The form for adding books is not currently using a CSRF token. This means that when you are visiting another website while logged in to BugBeat, your browser could be told to send a request to BugBeat that adds a book to your account.

With Django, this is easy to fix. First of all, you have to remove the csrf_exempt-annotation above the add_book function on line 31 in views.py. Then you have to add the CSRF token to the form by uncommenting line 48 in index.html.

**FLAW 3: Cross-Site Scripting**

Line: index.html line 21

When listing the books, the names of the books are assumed safe, meaning that a cross-site scripting attack would be possible. For example, by adding a book with the name `<script>alert("Something bad is happening")</script>`, reloading the page will result in you getting an alert from the site saying "Something bad is happening!".

To fix this, you can just remove the "safe" keyword on index.html line 21 so that the line would only be `{{book.book_name}}`. Now when you try to input the malicious text, you can just see that a book is added with the inputted name. However, reloading the page is no longer running the script as the text is now escpaed before it's embedded to the site.

**FLAW 4: Broken access control**

Line: views.py line 57

Currently it's not check whether the user marking a book read or unread is the actual reader of the book. This means that a user could set another user's book as read or unread if they knew or guessed the book's id. 

This can be prevented by uncommenting lines 59-60 in views.py. Now if a user tries to mark another user's book as read or unread, they would just be redirected to the home page without anything actually happening.

**FLAW 5: Broken authentication**

The registration currently uses no password validation. This means that short, well-known or otherwise weak passwords can be used.

Django has password validation functionalities built in. Those can be configured in server/settings.py by changing the items in the AUTH_PASSWORD_VALIDATORS list. To enable the password validation, uncomment the import on line 6 in views.py as well as lines 20 and 21 of the same file. With the fix applied, we should get rid of at least the most common problems in the users' passwords.