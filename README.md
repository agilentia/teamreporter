# Sherpany Boomerang

Allows creation and collection of reports to teams by email

### Version
0.0.1
### Installation

Note: This has only been tested on Ubuntu 14.04

```sh
$ git clone git@github.com:agilentia/teamreporter.git
$ cd teamreporter
$ virtualenv ~/.virtualenvs/sher #uses python3.4
$ source ~/.virtualenvs/sher/bin/activate
$ pip install -r requirements.txt
$ bower install #(depends on your system, but this requires node.js and npm)
$ python manage.py migrate
$ python manage.py loaddata teamreporter/fixtures/roles.json #seeds roles
$ heroku local web
$ Go to http://localhost:5000
```

### TODO
* Add ability to add questions through frontend (coming soon)
* Add period options for Team reports
* Start writing Angular unit/integration tests
* Write more Django unit tests 
* Add actual background job that sends, receives, parses, and saves answers from each team member
* Start adding comments

### Improvements
* Some angular code can be refactored into common packages.  In progress
* Return model fields in API calls so nothing needs to be hardcoded in angular
