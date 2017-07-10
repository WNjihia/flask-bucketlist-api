[![Codacy Badge](https://api.codacy.com/project/badge/Grade/93600bb65a2d4e51b0659003115ea6d6)](https://www.codacy.com/app/WNjihia/flask-bucketlist-api?utm_source=github.com&utm_medium=referral&utm_content=WNjihia/flask-bucketlist-api&utm_campaign=badger)
[![Build Status](https://travis-ci.org/WNjihia/flask-bucketlist-api.svg?branch=master)](https://travis-ci.org/WNjihia/flask-bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/WNjihia/flask-bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/WNjihia/flask-bucketlist-api?branch=develop)

### BucketList API

According to the Oxford Dictionary, a BucketList is a number of experiences or achievements that a person hopes to have or accomplish during their lifetime.

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
![Alt text](https://image.ibb.co/gsQT4a/Screen_Shot_2017_07_10_at_14_34_15.png)

**To Login a user**
![Alt text](https://image.ibb.co/csyTLF/Screen_Shot_2017_07_10_at_12_31_28.png)

**Create a new BucketList**
![Alt text](https://image.ibb.co/dbq9cv/Screen_Shot_2017_07_10_at_14_39_18.png)

**Get all BucketLists**
![Alt text](https://image.ibb.co/gEhAZa/Screen_Shot_2017_07_10_at_12_35_12.png)

**Get a single BucketList**
![Alt text](https://image.ibb.co/cwy1qF/Screen_Shot_2017_07_10_at_14_43_33.png)

**Update a BucketList**
![Alt text](https://image.ibb.co/g0jDnv/Screen_Shot_2017_07_10_at_12_34_35.png)

**Delete a BucketList**
![Alt text](https://image.ibb.co/jmhYnv/Screen_Shot_2017_07_10_at_12_34_59.png)

**Create a new BucketList item**
![Alt text](https://image.ibb.co/jjFa0F/Screen_Shot_2017_07_10_at_12_36_39.png)

**Get all BucketList items**
![Alt text](https://image.ibb.co/j0iRqF/Screen_Shot_2017_07_10_at_12_36_53.png)

**Get a single BucketList item**
![Alt text](https://image.ibb.co/mhC5Hv/Screen_Shot_2017_07_10_at_14_42_10.png)

**Update a BucketList item**
![Alt text](https://image.ibb.co/ifFvja/Screen_Shot_2017_07_10_at_12_37_50.png)

**Delete a BucketList item**
![Alt text](https://image.ibb.co/e6pAHv/Screen_Shot_2017_07_10_at_12_38_13.png)

**Search for:**
 **-a BucketList**
![Alt text](https://image.ibb.co/fnYvHv/Screen_Shot_2017_07_10_at_14_36_31.png)

 **-an Item**
![Alt text](https://image.ibb.co/imZfja/Screen_Shot_2017_07_10_at_14_35_56.png)

**Pagination**
![Alt text](https://image.ibb.co/kPcYnv/Screen_Shot_2017_07_10_at_12_33_08.png)

![Alt text](https://image.ibb.co/f3dHEa/Screen_Shot_2017_07_10_at_12_33_24.png)

### Testing

To test, run the following command:
```
nosetests
```
