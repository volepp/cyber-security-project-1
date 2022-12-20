# CBS Project 1

## Installation

You can install the required dependencies using `pip install -r requirements.txt` either globally or in a virtual environment if you choose to create one with e.g. [venv](https://docs.python.org/3/library/venv.html).

## Flaws

**FLAW 1: SQL injection**

views.py row 67

Example query: ' and 1==0 UNION SELECT 0, username || " " || password, 0 FROM auth_user;--

**FLAW 2: CSRF**

TODO: complete the description

views.py row 20

index.html row 39

**FLAW 3: Cross-Site Scripting**

Idea: allow css when adding a book

**FLAW 4: Broken access control**

TODO: complete the description

views.py row 48

**FLAW 5: Broken authentication**

Idea: also store the passwords in plain text when registering so that you can get them through SQL injection