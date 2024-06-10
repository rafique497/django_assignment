# django_assignment
## Steps to set up the project:

### Manual setup

* create a python3.8 environment and activate it (python or python3 -m venv environment_name)
* activate (environment_name/Scripts/activate for windows or source environment_name/bin/activate)
* install all the requirements 
    > pip install -r requirements.txt
* Please look setting.py and setup database
      DB_NAME=postgres  
      USERNAME=postgres  
      DB_PASSWORD=''  
      DB_HOST=db  
      DB_PORT=5432
    your project requirements, and then do the migrations
    >   python manage.py makemigrations
* and now time to migrate the changes
    > python manage.py migrate
* then run the server
    > python manage.py runserver
## http://127.0.0.1:8000/api-doc/  swagger docs

