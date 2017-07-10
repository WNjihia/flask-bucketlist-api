### BucketList api

According to the Oxford Dictionary, a bucketlist is a number of experiences or achievements that a person hopes to have or accomplish during their lifetime.

This is a Flask API for an online BucketList service.

### Installation and Setup

Clone the repository from GitHub:
```
$ git clone https://github.com/WNjihia/flask-bucketlist-api.git
```

Fetch from the develop branch:
```
$ git fetch origin develop
```

Navigate to the `flask-bucketlist-api` directory:
```
$ cd flask-bucketlist-api
```

Create a virtual environment:
> Use [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Install the required packages:
```
$ pip install -r requirements.txt

```

Install postgres:
```
brew install postgresql
type psql in terminal.
On postgres interactive interface, type CREATE DATABASE flask_api;
```

Create a .env file and add the following:
```
source name-of-virtual-environment/bin/activate
export FLASK_APP="run.py"
export SECRET="a-secret-key"
export DATABASE_URL="postgresql://localhost/flask_api"
```

Then run:
```
source .env
```

Run the migrations:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Launch the program:
```
python run.py
```

### API Endpoints

| Methods | Resource URL | Description | Public Access |
| ---- | ------- | --------------- | ------ |
|POST| `/api/v1/auth/login` | Logs a user in| TRUE |
|POST| `/api/v1/auth/register` |  Register a user | TRUE |
|POST| `/api/v1/bucketlists/` | Create a new bucket list | FALSE |
|GET| `/api/v1/bucketlists/` | List all the created bucket lists | FALSE |
|GET| `/api/v1/bucketlists/<bucketlist_id>/` | Get single bucket list | FALSE |
|PUT| `/api/v1/bucketlists/<bucketlist_id>/` | Update this bucket list | FALSE |
|DELETE| `/api/v1/bucketlists/<bucketlist_id>/` | Delete this single bucket list | FALSE |
|POST| `/api/v1/bucketlists/<bucketlist_id>/items/` | Create a new item in bucket list | FALSE |
|GET| `/api/v1/bucketlists/<bucketlist_id>/items/` | List items in this bucket list | FALSE |
|GET| `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>/` | Get single bucket list item | FALSE |
|PUT|`/api/v1/bucketlists/<bucketlist_id>/items/<item_id>/` | Update a bucket list item | FALSE |
|DELETE|`/api/v1/bucketlists/<bucket_id>/items/<item_id>/` | Delete an item in a bucket list | FALSE |
|GET| `/api/v1/bucketlists?limit=2&` | Pagination to get 2 bucket list records per page | FALSE |
|GET| `/api/v1/bucketlists?q=bucket` | Search for bucket lists with name like ```bucket``` | FALSE |
|GET| `/api/v1/bucketlists/<bucketlist_id>/items?limit=2&` | Pagination to get 2 bucketlist item records per page | FALSE |
|GET| `/api/v1/bucketlists/<bucketlist_id>/items?q=climb` | Search for bucketlist items with name like ```climb``` | FALSE |

### How to use the API

**Register a user**
**To Login a user**
**Create a new BucketList**
**Get all BucketLists**
**Get a single BucketList**
**Update a BucketList**
**Delete a BucketList**
**Create a new BucketList item**
**Get all BucketList items**
**Get a single BucketList item**
**Update a BucketList item**
**Delete a BucketList item**
**Search for:
 -**a BucketList**
 -**an Item**
**Pagination**

### Testing

To test, run the following command:
```
nosetests
```
