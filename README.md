# Banistmo Backend: A challenge

A *Django* App. Meant as a display of some backend programming skills.  A Frontend App is also available [here](https://github.com/sansagara/banistmo).
This is already deployed to Heroku for convenience. It can be found on [banistmo-back.herokuapp.com](http://banistmo-back.herokuapp.com/)

An index of the whole set of resources is available on [banistmo-back.herokuapp.com](http://banistmo-back.herokuapp.com/index.html)

## Running Locally

Make sure you have:
 - Python 3.6 [installed](http://install.python-guide.org) - see guides for [OSX](http://docs.python-guide.org/en/latest/starting/install3/osx/), [Windows](http://docs.python-guide.org/en/latest/starting/install3/win/) and [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/)
 - [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) installed locally. Accomplish this by running `pip install pipenv`.
 - [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup) installed locally.

```sh
$ git clone git@github.com:sansagara/banistmo.git
$ cd banistmo

$ pipenv --three
$ pipenv install
$ pipenv shell

$ createdb banistmo

$ python manage.py migrate
$ python manage.py collectstatic

$ python manage.py runserver
```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## Deploying to Heroku

This project is already configured to be run on heroku easily. If you want to make your own deployment, follow these instructions:
 - Create a free [Heroku Account](https://signup.heroku.com/signup/dc)
 - Install the [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli) for your system.
 - Login using the account details you used then creating your Heroku account.
```sh
$ heroku login
```
 - Prepare the app.
```sh
$ git clone git@github.com:sansagara/banistmo.git
$ cd banistmo
```
 - Deploy the app
```sh
$ heroku create
$ git push heroku master
```
 - Ensure that at least one instance of the app is running
 ```sh
 heroku ps:scale web=1
 ```
 - Install the [postgresql addon](https://elements.heroku.com/addons/heroku-postgresql) for the app.
 ```sh
 https://elements.heroku.com/addons/heroku-postgresql
 ```
  - Migrate the database and open
```sh
$ heroku run python manage.py migrate
$ heroku open
```
or instead, click on this button to deploy automatically:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://github.com/sansagara/banistmo-backend)

### Administrate
The Django Admin page can be used to make CRUD operations on Users and Transactions.
The superadmin username and password for the Live deployment is `Banistmo:Banistmo123`

## Dataset
This comes with a [companion dataset](transactions/management/dataset.csv). It can be inserted to your chosen database backend with the `import_dummy_data` management command.
You can run it with `python manage.py import_dummy_data`.

### About the Dataset
- The identifier of the rows is zero-indexed.
- The date may require parsing before being inserted into a DB engine.
- The UUID must be an integer.
- The TXN must be a signed decimal.
- Records with a missing date should be inserted, but considered in the results.
- The records with missing date must be shown to the end user in some way, without affecting aggregates or accounts.

For more info, view the R Notebook [here](http://rpubs.com/sansagara/banistmo)

## API
This is a RESTFul application made as the backend for a [Single-page Application](https://en.wikipedia.org/wiki/Single-page_application) (SPA) or App. A companion app was also developed and is available [here](https://github.com/sansagara/banistmo)
The API is done with [django-rest-framework] and [Djoser].
Each API endpoint is browsable, which means it can be checked on the browser to check its purpose and inspect results.
[Authentication](http://www.django-rest-framework.org/api-guide/authentication/) is possible via Session (for the browsable API) and Token (For the SPA).

### API Docs
The API docs can be found on the `/transactions/docs` route. On the already deployed application, it can be found [here](http://banistmo-back.herokuapp.com/transactions/docs/)

### Postman Collection
A postman collection is provided for convenience.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b0355bf3e36511d2c209)

## Async API responses
One of the requirements for the challenge involved coming up with a solution for long-running API endpoints on an async manner.
There are multiple ways to handle this scenario: task schedulers, threads, and queues. 
I went the queue route with [Redis](https://redis.io/), as it is lightweight, open-source and easy to install and setup.
This will allow to set a worker, who will dispatch API requests as server resources become available, using Redis queue system.

### Install
You can [install redis](https://redis.io/download) on your local system. 
However, a [Redis Heroku addon](https://elements.heroku.com/addons/heroku-redis) is also available and you can use it even for your local installation.
The Redis URL for the [Live](http://banistmo-back.herokuapp.com/) deployment in case you want to use it is:
 `redis://h:pdd34a64d7788396ebae5316a9fad2c46e77c3bdca863b4706d3c8aa4a7119e31@ec2-34-239-85-133.compute-1.amazonaws.com:32939`
The project's Procfile is set to automatically start workers on deployments.

### Setup
[Django-rq](https://github.com/ui/django-rq) is used to simplify setup. Just specify the URL of the redis service on the `RQ_QUEUES` on `settings.py`
```python
RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'), # R
        'DEFAULT_TIMEOUT': 500,
    },
}
```

### Endpoints
- To make a new request: `/service2/enqueue/` ([Live](http://banistmo-back.herokuapp.com/transactions/service2/enqueue/))
- To poll for a response: `/service2/poll` ([Live](http://banistmo-back.herokuapp.com/transactions/service2/poll/123))


### Administrate
The queues information can be seen from the Django Admin page, specifically on `/queues`. ([Live](http://banistmo-back.herokuapp.com/queues)).

## Documentation

### Django in general
- https://www.djangoproject.com/
- http://www.django-rest-framework.org/
- https://github.com/sunscrapers/djoser

### Async API
- https://github.com/ui/django-rq
- https://redis.io/
- https://stackoverflow.com/questions/32681602/django-rest-framework-make-asynchronous-request-to-respond
- https://stackoverflow.com/questions/27881706/why-should-i-build-an-api-with-an-asynchronous-non-blocking-framework


## About
#### Author
[Leonel Atencio](http://blog.leonelatencio.com)
#### Version
1.0
#### License
Do What The F*ck You Want To Public License (wtfpl)