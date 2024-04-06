# csb-project1

LINK: https://github.com/iidaw/csb-project1

This project uses OWASP 2021 list.

## Installation and usage
This project has been done using Python and Django.
1. Clone the repo
2. Start the app by ```python3 manage.py runserver``` (in the directory that has manage.py)
3. Make the needed migrations with following commands: <br>
   ```python3 manage.py makemigrations``` <br>
   ```python3 manage.py migrate```
5. Log in using username ```alice``` and password ```redqueen``` or username ```bob``` and password ```squarepants```

## FLAW 1: Broken Access Control
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L28

### Description
Broken access control is a security flaw that occurs when an application fails to properly enforce restrictions on what authenticated users are allowed to access. This vulnerability can enable unauthorized users to view sensitive data, modify data, or perform actions that they shouldn't have permissions for. 

The note route gets note id as a parameter when doing the GET request to see a spesific note ```note/<note:id>```. The user can just see other notes (not made by them) by inserting ```/note/<note:id>``` to the URL. 

### How to fix it
This flaw can be fixed by making sure that the current user actually "owns" the requested note. The route should also be changed to just ```note/``` so that it is not possible to access the notes straight from the URL.

Links to fixes in the code:
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L27
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L81
- Fix in urls.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/urls.py#L8


## FLAW 2: Cross-Site Request Forgery (CSRF)
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L18 <br>
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L69

### Description
Cross-Site Request Forgery (CSRF) is a security vulnerability that occurs when an attacker tricks a user's browser into making unintended requests to a web application. This is done by exploiting the trust that a site has in a user's browser and can lead to unauthorized actions being performed on behalf of the user without their consent.

### How to fix it
This flaw can be fixed making sure that the route requires a CSRF token. The CSRF token needs to be added to the form as well. This fix is relatively simple as I had to intentionally make this vulnerability by adding ```@csrf_exempt```, because Django is quite good with this on its own.

Links to fixes in the code:
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L15
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L65
- Fix in add_note.html form: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/templates/notes/add_note.html#L9

## FLAW 3: Cryptographic Failures
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L28

### Description
Cryptographic failures refer to security vulnerabilities stemming from incorrect or inadequate implementation of cryptographic techniques or algorithms. Cryptography plays a crucial role in securing sensitive data by ensuring confidentiality, integrity, and authenticity. When cryptographic mechanisms are improperly applied, attackers may exploit weaknesses to bypass security controls, gain unauthorized access to data or perform other malicious actions. In this project the ```SECRET_KEY```is hardcoded into ```settings.py```. An attacker can easily find the secret key. This project also has ```DEBUG=True```which allows the attacker to gain vulnerable information.

### How to fix it
These flaws can be fixed by adding an ```.env``` file with the ```SECRET_KEY``` and ```ÌS_DEV```. This way the secret key isn't straight in the code and the debug is disabled when the app is in production. The ```.env``` file should be in the ```.gitignore``` file so it won't be accessible in the repository.

Links to fixes in the code:
- Fix in settings.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L26
- Fix in settings.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L32


## FLAW 4: Injection (Cross-Site Scripting (XSS)
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L69
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L81 (settings.py intentionally disabled escaping)

### Description
Injection is a security vulnerability that occurs when untrusted data is inserted into an application and interpreted as code by the interpreter. This allows attackers to inject malicious code, such as SQL queries or JavaScript, into the application, leading to unauthorized access, data manipulation, or other malicious actions. In this project the note adding isn't protected against XSS attacks. 

### How to fix it
This flaw can be fixed by adding validation to the notes so that they aren't interpreted as HTML and/or JavaScript. Django is quite good with this on its own. I had to intentionally cause these vulnerabilities.

Links to fixes in the code:
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L70
- Fix in settings.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L81


## FLAW 5: Security Misconfiguration
https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L28

### Description
Security misconfiguration refers to the improper setup or configuration of security controls within a web application or its underlying infrastructure. This vulnerability can result from oversight, lack of awareness, or incorrect implementation of security measures. Security misconfigurations can leave systems vulnerable to various attacks, including unauthorized access, data breaches and service disruptions. In this project the error information is too informative and gives away too much information when trying to access notes with index number that doesn't exist as it is an error when the site is not found.

### How to fix it
This flaw can be fixed with a few different approaches. It can be modified in the ```views.py```file and have it return a modified error message or simply switching ```DEBUG=True``` to ```DEBUG=False```in ```settings.py```.

Links to fixes in the code:
- Fix in views.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes/views.py#L39
- Fix in settings.py: https://github.com/iidaw/csb-project1/blob/main/notes_app/notes_app/settings.py#L32
