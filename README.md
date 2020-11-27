### CAFM - Identity

This is a microservice that is responsible for managing the identity and access.

### Local Development
##### Requirements:  
**1 - All infra service are up and running**  
If you don't have them already running then you can do it by following this [link](https://github.com/DigitalMOB2/cafm.infra)  
**2 - Install Pipenv**  
You can run `pip install pipenv` in order to install Pipenv

##### Running the services (without docker)
**1 - Set up the env vars**  
Make a copy of .env.docker-compose and rename it to .env, then set up the ports for the following
based on the ports of the infrastructure services that you got from [CAFM.Infra Repo](https://github.com/DigitalMOB2/cafm.infra):  
`MESSAGE_BROKER_SERVERS - For kafka`  
`MESSAGE_SCHEMA_REGISTRY_URL - As stated for schema registry url`  
`CAFM_API_REDIS_PORT - As stated for redis`  
`CAFM_IDENTITY_ARANGODB_URL - As stated for arango db`

You need also to add in your /etc/hosts the following for kafka to work from the admin script:
`127.0.0.1 kafka`  
Also rename `src/resource/script/.env.sample` into `src/resource/script/.env`

**2 - Install the dependencies**  
`Pipenv install`   

**3 - Install hupper for watching and restarting the processes (Optional)**  
`pip install hupper`

**4 - Init kafka topics and schemas**  
Open the terminal go to src/resource/script of this repo, then issue the following commands:
`pipenv shell`  
`pipenv install`  
**You need python 3 and higher to run the script**
`python admin_script.py`  This will print the help, now issue the command  
`python admin_script.py init-kafka-topics-and-schemas`

And you should get:  
```sh
Topic cafm.identity.cmd created
Topic cafm.identity.evt created
```
Now if you visit the link http://localhost:8080/ (check the port from the [CAFM.Infra Repo](https://github.com/DigitalMOB2/cafm.infra)), 
then goto to menu '*topics*', then you will see the topics cafm.identity.cmd and cafm.identity.evt (as they set in the .env file). Also
if you visit the menu '*Schema Registry*', then you will see 2 schemas created cafm.identity.Command and
cafm.identity.Event (as they are set in the .env file)

**5 - Init the database**
`python admin_script.py init-db`  in order to create the collections and resources
You should see the following:  
```sh
Initialized the database
Create database cafm-identity if not exist
Create collections:
Create edges:
```  
Then we need to create a super admin user:
`python admin_script.py assign-user-super-admin-role arkan 1234 cafm-identity`  
It means create a user *arkan* with password *1234* in the database *cafm-identity*, this
database is created with the above command 'init-db' and it used the env var 
*CAFM_IDENTITY_ARANGODB_DB_NAME* that is in *.env* file

**6 - Run the API**
You need to open 3 terminals windows:
* One for kafka consumer to consume the commands from the api **Start at the root of this repository**
```sh
pipenv shell
hupper python -m src.port_adapter.messaging.listener.api_command.ApiCommandListener
```
* One for kafka consumer to consume the commands from the identity  
```sh
pipenv shell
hupper python -m src.port_adapter.messaging.listener.identity_command.IdentityCommandListener
```
* One for running grpc server for serving the requests from other microservices (e.g. api microservice)
```sh
pipenv shell
python -m src.port_adapter.api.grpc.server
```
  
##### Running the services (with docker compose)
**1 - Modify the environment variables**  
In the `.pkg/local/docker/Dockerfile` use the variables that you get from the infra (see [here](https://github.com/DigitalMOB2/cafm.infra))
  
**2 - Build the image and run the services**  
Run `docker-compose -f .pkg/local/docker/docker-compose.yaml -p cafm-identity up` from the root of this repository

**3 - Stop/Run the services**  
To stop the services, run `docker-compose -f .pkg/local/docker/docker-compose.yaml -p cafm-identity stop`  
To start the services, run `docker-compose -f .pkg/local/docker/docker-compose.yaml -p cafm-identity start`