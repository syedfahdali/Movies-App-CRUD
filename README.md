# Setup:
To install all required packages run 'pip install -r requirements.txt'\
Run the main.py file to start the site, click the ip in the console or go to http://127.0.0.1:80 in your browser to view the site.

# Adding new pages:
When creating a new blueprint (for example see website/pages/home/home.py) add it to `__init__.py` with 'app.register_blueprint(name_here)' to make sure Flask loads it.\
When you add a new .html page to the website/pages/dynamic_pages/templates folder it will be accessible in the browser by using the name of that html file (see other examples in the dynamic_page folder).

# Database:
The database/models.py file contains the ORM mappings for the database. All classes in this file that inherit db.Model 
will be added to the database when no database exists yet. Sometimes when changing the models or adding new ones they 
can not be added to the database, in this case manually adding the changes to the database is necessary or simply 
deleting the entire database will also solve this problem. By default, the app.db file is the database.
#   M o v i e s - A p p - C R U D -  
 