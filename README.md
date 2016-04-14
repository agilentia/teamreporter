# Sherpany Boomerang

[Boomerang](https://github.com/agilentia/teamreporter) is an application that helps you to get status updates from your team in an easy and automated way.

Boomerang was inspired by [Teamreporter](http://www.teamreporterapp.com/), which ended its operations in 2016-April.

### Version
0.0.2

### Installation

Note: This has been tested on Ubuntu 14.04 and OS X 10.11.3

```sh
$ git clone git@github.com:agilentia/teamreporter.git
$ cd teamreporter
$ mkvirtualenv -p python3 boomerang
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
* Start adding comments
* Take roles into account for user / report management

### Improvements
* Some angular code can be refactored into common packages.  In progress
* Return model fields in API calls so nothing needs to be hardcoded in angular

## Team

* **Ânderson Quadros** - [anquadros](https://github.com/anquadros) - *Initial work*
* **Daniel Borzęcki** - [borzecki](https://github.com/borzecki) - *Initial work*
* **Mathias Brenner** - [mathiasbrenner](https://github.com/mathiasbrenner) - *Initial work*
* **Tony Lambropoulos** - [tony7126](https://github.com/tony7126) - *Initial work* 

## Contributors

Please use the [issue tracker](https://github.com/agilentia/teamreporter/issues) to report any bugs or file feature requests.

## License

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) - see the [LICENSE.txt](https://github.com/agilentia/teamreporter/blob/master/license) file for details.

## Thanks

Thanks to [Sherpany](http://www.sherpany.com/) for putting the team together. 
