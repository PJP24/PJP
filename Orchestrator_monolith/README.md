Project Setup

Follow the steps below to set up and run the project locally:

1. Create a Virtual Environment
Create a Python virtual environment to manage project dependencies:
python3 -m venv venv

2. Activate the Virtual Environment
Activate the virtual environment:
source venv/bin/activate

3. Install Dependencies
Use the Makefile to install project dependencies:
make install

4. Start Colima
Run 'colima start' in terminal, or install it first

5. Start Docker containers
In terminal run 'make start' to start the app

6. Run 'make stop' to stop the containers

Notes
- Ensure Docker is running on your machine before executing the make docker_start command.
- This setup assumes you have make installed on your system. If not, install it via your package manager.
- Run make test to run pytest, if you encounter any issues most likely it's due to the PYTHONPATH import. To fix run: 
'export PYTHONPATH=$PYTHONPATH:$(pwd)' in current terminal window, then try again.

---

Feel free to contribute or report issues if you encounter any.