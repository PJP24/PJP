# Steps to start the users server

### Create and start venv:
```make init ```

### Install requirements:
```pip3 install -r requirements.txt```


### Run the containers which will start the DB and the users server:
``` docker-compose up --build -d ```

### Create the users table
```alembic upgrade head```


### To start the client and test the server:
```make client```


#### pgAdmin for db visualization
To log into Pgadmin:
* go to: http://localhost:8080/browser/
* Add New Server: 
* Name: grpc 
* host name: postgres
* username: test
* password: test123