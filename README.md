# Flask-React-SQLite Boilerplate

This project simplifies spinning up a new app or idea by providing a boilerplate web app skeleton. It includes a React (JavaScript) frontend, Flask (Python) backend, and an Sqlite database. 

- [License](#license)
- [Installation](#installation)
- [Usage](#usage)
- [Database](#database)
  - [Tables](#tables)
  - [Migrations](#migrations)
  - [Command-line Database Access](#command-line-database-access)
  - [Version Control](#version-control)
- [Backend](#backend)
  - [Endpoints](#endpoints)
  - [Reset Handlers](#reset-handlers)
  - [GET Requests](#get-requests)
  - [POST Requests](#post-requests)
- [Frontend](#frontend)
  - [Favicons](#favicons)
  - [App Title](#app-title)
  - [BackendAPI Module](#backendapi-module)
  
## License

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

I hereby relinquish all copyright interest in all content in this repository, and dedicate it to the world-wide public domain. I have opted out of copyright entirely. I disclaim all warranties and am neither restricting nor responsible for your use of this material. 

## Installation

The app works on at least the following versions:

- nodejs v12.18.3
- npm 6.14.8
- python v3.6.9
- flask 1.1.2
- sqlite3 3.32.1

```
sudo apt install nodejs python sqlite3
sudo npm install npm -g
sudo pip install flask
```

Clone the repository and rename it. These instructions assume a name of `newproject` created in the home directory and reachable at `~/newproject`.

```
cd ~/
git clone https://github.com/LawrenceXie/ProjectTemplate.git newproject
```

Install the frontend project.

```
cd ~/newproject/frontend
npm install
```

Install the backend as a package.

```
cd ~/newproject/backend
pip install -e .
```

Set up the database.

```
cd ~/newproject/backend
flask db init
flask db stamp head
flask db migrate -m "Initial database migration"
flask db upgrade
```

## Usage

The app assumes `localhost:5000` for the backend and `localhost:3000` for the frontend. 

**There are four ways to run the program locally.**

1. Open two terminal windows. In the first, 

    ```
    cd ~/newproject/backend && flask run
    ```
    
    In the second, 
    
    ```
    cd ~/newproject/frontend && npm start
    ```

1. Open a single terminal window. The single ampersand in the following command moves the backend `npm start` process to the background, then calls the frontend `npm start` process. That allows both backend and frontend to run in the same window. If you `Ctrl+C` in that window, you first close the frontend. You can bring the backend to the foreground by running `fg`. Another `Ctrl+C` will then kill the backend process. You can close both processes at the same time by closing the entire terminal window.

    ```
    cd ~/newproject/backend && flask run & cd ../frontend && npm start
    ```

1. An optional script in this repository provides the following one-liner with relative paths: 

    ```
    cd backend && flask run & cd ../frontend && npm start
    ```

    To use the script, first set it user-modifiable:

    ```
    chmod u+x run.sh
    ```

    Then start the program by running the `run.sh` script:

    ```
    ./run.sh
    ```

1. Adding an alias to your `~/.bashrc` can be useful, though it expects an absolute path:

   ```
   alias newproject="cd ~/newproject/backend && flask run & cd ../frontend && npm start
   source ~/.bashrc
   ```

   Then you can run the command from any terminal window:

   ```
   newproject
   ```

## Database

The database will be a binary file called `db.sqlite` in `~/newproject/backend/backend/db`. 

Migrations will be tracked in `~/newproject/backend/migrations`.

If the database and migrations do not yet exist, use the database installation instructions:

```
cd ~/newproject/backend
flask db init
flask db stamp head
flask db migrate -m "Initial database migration"
flask db upgrade
```

### Tables

There are two tables, `admin` and `items`. 

SQLite handles the primary key `id` of the `admin` table, autoincrementing because it's an integer. However, it is assumed that React handles the primary key `id` of the `items` table, because it is specified as text. Change this to an integer if you want SQLite to handle it. Primary keys are required to be unique by definition.

#### Admin Table

|column|type|notes|
|------|----|-----|
|id|integer|primary key|
|key|text|not null|
|value|text|not null|
|format|text|not null|

#### Items Table

|column|type|notes|
|------|----|-----|
|id|text|primary key, not null|
|date_created|integer|not null|
|date_updated|integer|not null|
|text|text|not null|

### Migrations

Changes to the schema can be made by edting `~/backend/backend/models.py`, closing the frontend and backend app processes, and running the following:

    ```
    cd ~/backend
    flask db stamp head
    flask db migrate -m "Add table tablename"
    flask db upgrade
    ```

Then restart the frontend and backend of the app.

### Command-line Database Access

The database can be accessed by the `sqlite3` command line tool. 

```
sqlite3 ~/newproject/backend/backend/db/db.sqlite
```

The following table shows useful forms of simple commands. See also: [SQLite Tutorial](https://www.sqlitetutorial.net/)

```
.schema
.table
SELECT * FROM admin
SELECT * FROM items
INSERT INTO admin (key, value) VALUES ('configvar1','true');
SELECT key, value FROM admin WHERE key = 'configvar1'
UPDATE admin SET value = 'false' WHERE key = 'configvar1'
DELETE FROM admin WHERE key = 'configvar1'
```

### Version Control

The `db.sqlite` database itself is a binary file and unsuited to version control. 

Instead, create and commit a backup `dump.sql` and `schema.sql`:

```
cd ~/newproject/backend/backend/db
sqlite3 db.sqlite .dump > dump.sql
sqlite3 db.sqlite .schema> schema.sql
git add .
git commit -m "Back up database"
```

## Backend

Flask provides a set of simple REST API endpoints and performs CRUD operations on the SQLite database.

The Flask webserver serves the endpoints from `localhost` at port `5000`. 

Bring up `http://localhost:5000/` in the browser or use curl from the terminal. For example,

```
curl http://localhost:5000/admin
```

### Endpoints

|address|returns|
|-------|-------|
|/|Congratulatory text string|
|/admin|Single JSON object with key-value pairs.|
|/admin/reset|Single JSON object with key-value pairs after the reset.|
|/items|List of JSON objects|
|/items/reset|List of new JSON objects after the reset.|
|/backup|Dump the database, commit the backup to git, return single JSON object.|

### Reset Handlers

The `reset` endpoints drop the appropriate table and rebuild it from test data defined in Flask. This comes in handy during development, but would not be exposed in production.

### Request Headers

The two endpoints `/admin` and `/items` only allows requests with `GET` and `POST` HTTP methods. 

#### GET Requests

`GET` Requests need to only specify the `GET` method in their request:

```
{
  method: 'GET'
}
```

#### POST Requests

`POST` Requests need to specify the `POST` method, a `Content-Type` in their headers, and a `body` JSON object that itself contains a variable called `method` to describe the type of request: `CREATE`, `READ`, `UPDATE`, `DELETE`.

For example, here is the expected packet of a request to create a new keypair in the `admin` table:

```
{
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: {
    'method': 'CREATE',
    'key': 'configvar2',
    'value': 'true'
  }
}
```

Here is the expected packet of a request to update an item whose ID already exists in the `items` table:

```
{
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: {
    'method': 'UPDATE',
    'id': '023adf31',
    'date_created': 1602883147,
    'date_updated': 1602891038,
    'text': 'This is newer, better, more updated text.'
  }
}
```

Requests to read a single packet only need the method and packet ID in the `body`:

```
{
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: {
    'method': 'READ',
    'id': '023adf31',
  }
}
```

Similarly, requests to delete a packet only need the method and packet ID in the `body`:

```
{
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: {
    'method': 'DELETE',
    'id': '023adf31',
  }
}
```

## Frontend

The React frontend was created with `create-react-app`. 

### Favicons

The app comes with placeholder favicons. I generate new favicons with the free [Favicon Generator](https://favicon.io/). Place the new icons in the `~/newproject/frontend/public` folder and update the `index.html` and `manifest.json` files as necessary.

### App Title

Update `~/newproject/frontend/public/index.html` to have the correct app title.

### BackendAPI Module

The frontend includes a BackendAPI module to call the CRUD operations we defined in the Flask backend. 


