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

4. Generate gRPC Files
Generate the necessary gRPC files using the Makefile:
make grpc

5. Start Docker Containers
Start the required Docker containers:
make docker_start

6. (Optional) Stop Docker Containers
If you need to stop the Docker containers, you can use the following command:
make docker_stop

7. Test the endpoint in any client with a post request to http://localhost:5001/orchestrate in a json format {
  "user_id": "1 to 10"
}


Notes
- Ensure Docker is running on your machine before executing the make docker_start command.
- This setup assumes you have make installed on your system. If not, install it via your package manager.

---

Feel free to contribute or report issues if you encounter any.