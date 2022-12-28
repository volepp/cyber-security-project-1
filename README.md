## Installation

After cloning the repository, you should be able to install all the required dependencies by running “pip3 install -r requirements.txt” in the project’s root directory. You can also set up a virtual environment and install the dependencies there if you’d like (instructions here: https://docs.python.org/3/library/venv.html). The project only requires Django as an external dependency.

Before running for the first time, run “python3 manage.py migrate” in the project root to get the database schema set up correctly. After that you should be able to start the server by running “python3 manage.py runserver”.

You can add accounts from the login page using the registration form that’s located under the login form. The server creates a db.sqlite3 file in the project root. You can remove all the added books and accounts by deleting that file.

The flaws are from the 2017 OWASP top ten web application security risks list.

### Flaw 1: SQL injection

Line: https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/views.py#L72 

The application currently allows the user to perform a successful SQL injection attack using the search field on the front page. By using the sqlite3 cursor and forming the SQL query manually in the code without using a parameterized query, it's possible to input a malicious text such as “' and 1==0 UNION SELECT 0, username || " " || password, 0 FROM auth_user;--” (make sure you include the single quotation mark in the beginning when copying), which would fetch all the usernames and passwords from the database.

To fix this, a parameterized query could be used. By using the currently commented line 74 instead of line 77, the malicious input won't work anymore. Another way would be to just use the model's filter function. Then you wouldn't have to use the sqlite3 library directly at all. To apply this fix, uncomment the lines 76 and 80-81 in views.py and use those instead of lines 77 and 82-83 that are currently in use.

### Flaw 2: CSRF

Line: https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/views.py#L29 and https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/templates/pages/index.html#L46 

The form for adding books is not currently using a CSRF token. This means that when you are visiting another website while logged into BugBeat, your browser could be told to send a request to BugBeat that adds a book to your account. Without using a CSRF token in the form, the application would have no way of knowing whether the request was sent by you or by some script that was run in your browser when loading a malicious website.

With Django, this is easy to fix. First of all, you have to remove the csrf_exempt-annotation above the add_book function on line 31 in views.py. Then you have to add the CSRF token to the form by uncommenting line 48 in index.html.

### Flaw 3: Cross-Site Scripting

Line: https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/templates/pages/index.html#L19 

When listing the books, the names of the books are assumed safe, meaning that a cross-site scripting attack would be possible. For example, by adding a book with the name “<script>alert("Something bad is happening")</script>”, reloading the page will then result in you getting an alert from the site saying "Something bad is happening!". This is because the text you gave included a script that was directly embedded to the html due to the input being assumed safe and thus being left unescaped. Then when your browser is loading the site, it runs the script like it would run any other script that was included in the html.

To fix this, you can just remove the "safe" keyword on index.html line 21 so that the line would only be “{{book.book_name}}”. Now when you try to input the malicious text, you can just see that a book is added with the inputted name. However, reloading the page is no longer running the script as the text is now escaped before it's embedded to the html.

### Flaw 4: Broken access control

Line: https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/views.py#L57 

Currently it's not checked whether the user marking a book read or unread is the actual reader of the book. This means that a user could set another user's book as read or unread, if they knew or guessed the book's id, by sending a POST request to either “/read/” or “/unread/” and having the request parameter “book_id” set to some book’s id.

This can be prevented by uncommenting lines 59-60 in views.py. Now if a user tries to mark another user's book as read or unread, they would just be redirected to the home page without anything actually happening.

### Flaw 5: Broken authentication

Line: https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/views.py#L4 and https://github.com/volepp/cyber-security-project-1/blob/6f75cdc1f7bb7ca9dabb9dc1da18cb3654fc9113/cbs_project/views.py#L18 

The registration currently uses no password validation. This means that short, common or otherwise weak passwords can be used. This makes the application vulnerable to basic brute force and dictionary attacks that attempt to login with numerous simple or most commonly used passwords.

Django has password validation functionalities built in. Those can be configured in server/settings.py by changing the items in the AUTH_PASSWORD_VALIDATORS list. To enable the password validation, uncomment the import on line 6 in views.py as well as lines 20 and 21 of the same file. With the fix applied, the users won’t be able to use passwords that are too close to their username, too short, too common, or completely numeric.
