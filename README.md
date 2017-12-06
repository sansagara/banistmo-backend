# Banistmo: A challenge

A Django App. Meant as a display of some backend programming skills.

The whole set of resources are available on [banistmo.herokuapp.com](http://banistmo.herokuapp.com/)

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  
Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:sansagara/banistmo.git
$ cd banistmo

$ pipenv --three
$ pipenv install
$ pipenv shell

$ createdb banistmo

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)


## About the Dataset
- El identificador de las filas esta indexado en cero.
- La fecha puede requerir parseo antes de ser insertada en un manejador.
- El UUID debe ser un entero.
- El TXN debe ser un decimal signed.
- Los registros con fecha faltante deben ser insertados, pero considerados en los resultados.
- Los registros con fecha faltante deben mostrarse al usuario final de alguna manera, sin que afecte agregados o cuentas.

For more info, view the R Notebook [here](http://rpubs.com/sansagara/banistmo)

## Documentation
This comes with a [companion dataset](transactions/management/dataset.csv). It can be inserted to your chosen database backend with the `import_dummy_data` management command.
You can tun it with `python manage.py import_dummy_data`.

## Postman Collection
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b0355bf3e36511d2c209)

## Documentation
https://stackoverflow.com/questions/32681602/django-rest-framework-make-asynchronous-request-to-respond
https://stackoverflow.com/questions/27881706/why-should-i-build-an-api-with-an-asynchronous-non-blocking-framework
https://github.com/ui/django-rq
http://www.django-rest-framework.org/
https://redis.io/
