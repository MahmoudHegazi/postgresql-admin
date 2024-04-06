from setuptools import setup, find_packages
setup(
name='mypackage',
version='0.1.0',
author='Python king',
author_email='mahmod.hagzy@gmail.com',
description='This library is used to add a GUI endpoint to manage all Postgresql database schemas owned by the given Postgresql user, you can easily add it to any flask application by importing it and instantiating the pgAdmin class by providing your own Flask application class to it, postgresql-admin uses bootstrap4, It is characterized by a responsive design that makes the GUI look good and easy to use on the computer and mobile phone. Also, postgresql-admin may lag when starting because it gets all the data first, so after starting you can perform all your actions and view your data quickly and without time. It also... It uses AJAX and includes helper queries and actions that can make managing your postgresql task a breeze.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)


#Homepage="https://github.com/MahmoudHegazi/postgresql-admin",
#Issues = "https://github.com/MahmoudHegazi/postgresql-admin/issues"