# postgresql-admin

This library is used to add a GUI endpoint to manage all Postgresql database schemas owned by the selected Postgresql user, you can easy add it to any flask application by import it and create pgAdmin class instance by providing your Flask app class to it, postgresql-admin is using bootstrap4, and it have responsive desgin that make the GUI look good and easy to use on computer and mobile, also the postgresql-admin may delay when start as it get all data first so after it start you can do all your actions and view your data fast with no time, also it uses AJAX and include help quires and actions can make manage your postgresql task is easy.

![image](https://github.com/MahmoudHegazi/postgresql-admin/assets/55125302/6ee48190-9e7d-41f4-86a2-e70fc4ff8dee)



### full code example

```python
from flask import Flask, render_template, redirect, url_for, jsonify, flash, request
from postgresql_admin import pgAdmin

app = Flask(__name__, template_folder='templates', static_folder='static')

# add postgresql admin to your apps is easy as hello wiorld
pg_admin = pgAdmin(app)

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
pgAdmin(app)
```

### How to use
1- install library using command ```pip install postgresql-admin```
2- import postgresql_admin model at your __init__ file and provide app to pgAdmin class
3- start your python app ```python __init__.py``` or ```flask run``` or as the way required to start your flask app.
3- visit endpoint /postgresql-admin


# Author:
Python King (Mahmoud Hegazy)

