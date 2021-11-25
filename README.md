# P10_planat_loic

## Description

Project Django using Django REST Framework. 

The goal is to have an API which allow us to show issues from projects, detected by contributors.
We could create projects with contributors and for each project, contributors can add issues they found and write comments for each issues. 

***
## Requirements
Python 3 : https://www.python.org/downloads/
## Installation

In the terminal, move to the directory where you want to install the repository with the command line:
```
cd <pathdirectory>
```
Clone the remote repository:
```
git clone https://github.com/Yonohi/P10_planat_loic.git
```
Go into the new folder:
```
cd P10_planat_loic
```
Create the environment:
```
python3 -m venv env
```
Activate the environment:
On Unix and macOS:
```
source env/bin/activate
```
On Windows:
```
env\Scripts\activate.bat
```
Now, install packages from requirements.txt
```
pip install -r requirements.txt
```
Go into the folder named LITReview
```
cd SoftDesk
```
Run in local
```
python3 manage.py runserver
```
Now you can go to the address
```
http://127.0.0.1:8000/signup/
```
## How it works
### By POSTMAN:


At this address you can register or log in. If you want to see the different projects go to : 
```
http://127.0.0.1:8000/api/projects/
```
or the issues of the project (if you are contributor of the project) :
```
http://127.0.0.1:8000/api/projects/{id}/issues/
```
or the comments of an issue (if you are contributor of the project) :
```
http://127.0.0.1:8000/api/projects/{id}/issues/{id}/comments/
```
For more information about endpoint : 
## Need a superuser?
You have to go to the project folder and type
```
python3 manage.py createsuperuser
```
Now give your username, mail and password, and it's done. The admin page is reachable.
```
http://127.0.0.1:8000/admin/
```
## Information about database
Go to the folder where you have your database and type
```
sqlite3 db.sqlite3
```
You can see all the tables with
```
.tables
```
To see the content of a table.
```
select * from <nametable>;
```
## Conclusion
It was interesting to learn how to use Django REST Framework and to improve my knowledge about security.
## Author
Loïc Planat
