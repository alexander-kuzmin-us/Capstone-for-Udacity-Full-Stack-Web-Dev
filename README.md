# Capstone project for Udacity Full Stack Web Developer NanoDegree

## CHARTER COMPANY Specifications

The Charter Company is a company that is responsible for providing and managing charters and assigning crew members to those charters.
You are a Head of the Charter Department within the company and are creating a system to simplify and streamline your process.
In order to communicate with application, got to
[The Charter Company]() 
use the credentials for the different roles provided below in Roles to log in,
copy and use jwt_token to get endpoints.

### Models:

- `Charters` with the attributes charters_name and departure_date.

- `Skippers` with attributes name, age and gender.

### Endpoints:

- **GET** `/charters`

    To get all the charters in the db and displays them as json format.
```
curl -X GET \
  https://charterscompany.herokuapp.com/charters \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **GET** `/skippers`

    To get all the skippers in the db and displays them as json format.
```
curl -X GET \
  https://charterscompany.herokuapp.com/skippers \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```
- **POST** `/charters/create`

    To create a new Charter based on the json data in the body of the request.
```
curl -X POST \
  https://charterscompany.herokuapp.com/charters/create \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **POST** `/skippers/create`

    To create a new Skipper based on the json data in the body of the request.
```
curl -X POST \
  https://charterscompany.herokuapp.com/skippers/create \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **DELETE** `/charters/delete/int:charter_id`

    To delete the Charter with given Charter ID.
```
curl -X DELETE \
  https://charterscompany.herokuapp.com/charters/delete/int:charter_id \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **DELETE** `/skippers/delete/int:skipper_id`

    To delete the Skipper with given ID.
```
curl -X DELETE \
  https://charterscompany.herokuapp.com/skippers/delete/int:skipper_id \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **PATCH** `/skippers/patch/int:skipper_id`

    To modify the Skipper with given ID.
```
curl -X PATCH \
  https://charterscompany.herokuapp.com/skippers/patch/int:skipper_id \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

- **PATCH** `/charters/patch/int:charter_id`

    To modify the Charter with given ID.
```
curl -X PATCH \
  https://charterscompany.herokuapp.com/charters/patch/int:charter_id \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```
### Roles:

- `Charter Assistant`
Can view skippers and charters

Auth0 credentials: 
    username: 
    password: 

- `Charter Director`
All permissions a Charter Assistant has and 
add or delete a skippers from the database
Modify skippers or charters

Auth0 credentials: 
    username: 
    password: 
    
- `Head of the Charter Department`
All permissions a Charter Director has and 
add or delete a charter from the database

Auth0 credentials: 
    username: 
    password: 

### Tests:

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb test_db
python test_app.py
```
