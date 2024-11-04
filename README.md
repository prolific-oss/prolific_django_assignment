# Task

This repo has a basic API implementation which allows the creation and storing of data about studies, and submissions to those studies.

A study has a set number of available places, once this number of submissions has been received the study should be completed and no further submissions allowed.

The support team have recently received the following complaint from a researcher:

> I set my study to have 100 available places, but I've received 103 submissions. I can't afford to pay for all of these submissions.

## What to do

- Get the API set up and running.
- Identify the cause of the above bug, and write code to fix it.
- Write unit tests to cover this case, and ensure all tests are passing.

For the next part of the assignment, we would like you to:

- Extend the API to allow the submission list to be filtered for a specific user
- Perform a code review for the open pull request and offer comments for how it could be improved. Additionally, if you have any comments on the rest of the codebase and how you would refactor/improve it if you had the chance, please offer them too!

## Running the API

Install the latest version of python3

Clone and navigate to the repository

Install dependencies

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run tests

```shell
python manage.py test
```

Initialise database

```shell
python manage.py makemigrations prolific
python manage.py migrate
```

Run server (on localhost:8000)

```shell
python manage.py runserver
```

## API Endpoints

### GET /studies/

#### Description

Returns a list of all existing studies

#### Examples

List all studies in database

```shell
> curl -XGET "http://localhost:8000/studies/"

HTTP 200 OK
[
    {
        "id": 1,
        "name": "study1",
        "total_places": 1,
        "user_id": 1,
        "status": "COMPLETED"
    },
    {
        "id": 2,
        "name": "study2",
        "available_places": 1,
        "user_id": 2,
        "status": "COMPLETED"
    },
    {
        "id": 3,
        "name": "study3",
        "available_places": 1,
        "user_id": 2,
        "status": "ACTIVE"
    }
]
```

### POST /studies/

#### Description

Creates a new study

#### Request parameters

> **name**: _str_ Name of the study
> **total_places**: _int_ Maximum number of submissions allowed
> **user_id**: _int_ Owning user of the study

#### Examples

```shell
> curl -XPOST "http://localhost:8000/studies/" -d "name=study1&total_places=1&user_id=1"

HTTP 201 Created
{
    "id": 3,
    "name": "study3",
    "available_places": 1,
    "user_id": 2,
    "status": "ACTIVE"
}
```

### GET /studies/<int: study_id>/submissions/

#### Description

Returns a list of all submissions for a given study

#### Examples

List all submissions for a given study

```shell
> curl -XGET "http://localhost:8000/studies/1/submissions/"

HTTP 200 OK
[
    {
        "id": 1,
        "study_id": 1,
        "user_id": 2,
        "created_at": "2019-11-27T17:41:27.205398Z"
        "completed_at": "2019-11-27T17:44:32.115467Z",
        "status": "COMPLETED"
    }
]
```

### GET /submissions/

#### Description

Returns a list of all existing submissions

#### Examples

List all submissions in database

```shell
> curl -XGET "http://localhost:8000/submissions/"

HTTP 200 OK
[
    {
        "id": 1,
        "study_id": 1,
        "user_id": 2,
        "created_at": "2019-11-27T17:41:27.205398Z"
        "completed_at": "2019-11-27T17:44:32.115467Z",
        "status": "COMPLETED"
    },
    {
        "id": 2,
        "study_id": 2,
        "user_id": 1,
        "created_at": "2019-11-27T17:41:46.787398Z"
        "completed_at": "2019-11-27T17:43:17.215294Z",
        "status": "COMPLETED"
    },
    {
        "id": 3,
        "study_id": 3,
        "user_id": 1,
        "created_at": "2019-11-27T17:42:14.518398Z"
        "completed_at": null,
        "status": "ACTIVE"
    }
]
```

### POST /submissions/

#### Description

Creates a new submission

#### Parameters

> **study_id**: _int_ Study to respond to

> **user_id**: _int_ Owning user of the submission

#### Examples

```shell
> curl -XPOST 'http://localhost:8000/submissions/' -d "study_id=1&user_id=2"

HTTP 201 Created
{
    "id": 3,
    "study_id": 3,
    "user_id": 1,
    "created_at": "2019-11-27T17:42:14.518398Z"
    "completed_at": null,
    "status": "ACTIVE"
}
```

### POST /submissions/<int: submission_id>/

#### Description

Updates an existing submission

#### Parameters

> **action**: _str_ The update action to perform

#### Examples

```shell
> curl -XPOST 'http://localhost:8000/submissions/3' -d "action=complete"

HTTP 200 OK
{
    "id": 3,
    "study_id": 3,
    "user_id": 1,
    "created_at": "2019-11-27T17:42:14.518398Z"
    "completed_at": "2019-11-28T11:21:18.183351Z",
    "status": "COMPLETED_AT"
}
```
