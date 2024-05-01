# postgresql-admin

This library is used to add a GUI endpoint to manage all Postgresql database schemas owned by the given Postgresql user, you can easily add it to any flask application by importing it and instantiating the pgAdmin class by providing your own Flask application class to it, postgresql-admin uses bootstrap4, It is characterized by a responsive design that makes the GUI look good and easy to use on the computer and mobile phone. Also, postgresql-admin may delay a little when starting because it gets all the data first, so after starting you can perform all your actions and view your data quickly and without time. It also... It uses AJAX and includes helper queries and actions that can make managing your postgresql task a breeze (Very easy to setup and use, We provide real User expreince).

![image](https://github.com/MahmoudHegazi/postgresql-admin/assets/55125302/6ee48190-9e7d-41f4-86a2-e70fc4ff8dee)



### full Flask app code example
Make sure you replace postgres-user and postgresql-pass with your own postgresql user and password, you can also specify your default shecema or leave it as postgres but in this case make sure you provide the user with privileges to use postgres

```python
from flask import Flask, render_template, redirect, url_for, jsonify, flash, request
from postgresql_admin import pgAdmin

app = Flask(__name__, template_folder='templates', static_folder='static')

# add postgresql admin to your apps is easy as printing hello wiorld
pg_admin = pgAdmin(app, user="postgres-user", password="postgresql-pass", host="127.0.0.1", port="5432", default_shecema='postgres')

app.config['SECRET_KEY'] = 'your-app-secert'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True, use_reloader=True, port=4023)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #disable cache

```

Please note
```python
from postgresql_admin import pgAdmin
pgAdmin(app, user="postgres-user", password="postgresql-pass", host="127.0.0.1", port="5432", default_shecema='postgres')
```

### How to use
1. install library using command ```pip install postgresql-admin```
2. from postgresql_admin module import pgAdmin class at your __init__ file and provide app to pgAdmin class, and postgresql credentials
3. start your python app ```python __init__.py``` or ```flask run``` or as the way required to start your flask app.
4. visit endpoint /postgresql-admin


# Author:
Python King (Mahmoud Hegazy)

