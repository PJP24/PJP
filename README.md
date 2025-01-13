Project Setup

Follow the steps below to set up and run the project locally:

1. Choose orchestrator_jan dir and run all future commands from it.

2. Create and activate a Virtual Environment
Create a Python virtual environment to manage project dependencies:
'python3 -m venv venv'

3. Run 'source venv/bin/activate' to activate the venv

4. Install Dependencies
Use the Makefile to install project dependencies:
make install or run pip install -r requirements.txt

5. Start Colima
Run 'colima start' in terminal, or install it first running 'brew install colima'

6. Start Docker containers
In terminal run 'make start' to start the app

7. Run alembic migrations:
Open a new terminal. Run 'cd orchestrator_jan'. Then 'alembic -c user_service/alembic.ini upgrade head ', then 'alembic -c subscription_service/alembic.ini upgrade head',
if those commands are not working try 'export PYTHONPATH=$PYTHONPATH:$(pwd)' first

8. Go to the http://0.0.0.0:8001/graphql for starting the app

9. Run 'make stop' in terminal to stop the containers


---
IF YOU ARE ENCOUNTERING ANY ERRORS PLEASE CHECK THIS FIRST:
- Ensure Docker is running on your machine before executing the make docker_start command.
- If you encounter any issues most likely it's due to the PYTHONPATH import. To fix run: 
'export PYTHONPATH=$PYTHONPATH:$(pwd)' in current terminal window, then try again.
---

Feel free to contribute or report issues if you encounter any.
All necessary commands are at the end of the file. For additional info

pythonpath:
    export PYTHONPATH=$PYTHONPATH:$(pwd)

alembic: 
    alembic -c user_service/alembic.ini upgrade head 
    alembic -c subscription_service/alembic.ini upgrade head

protos:
    python -m grpc_tools.protoc -I=protos --python_out=user_service/grpc_services/generated --grpc_python_out=user_service/grpc_services/generated protos/user.proto
	python -m grpc_tools.protoc -I=protos --python_out=subscription_service/grpc_services/generated --grpc_python_out=subscription_service/grpc_services/generated protos/subscription.proto
