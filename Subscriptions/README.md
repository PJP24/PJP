Terminal Commands to Run Subscriptions Service

1. Navigate to Subscriptions Directory:
cd Subscriptions

2. Create Virtual Environment:
python3 -m venv venv

3. Activate the Virtual Environment:
source venv/bin/activate

4. Install Required Dependencies:
pip3 install -r requirements.txt

5. Add .env File:
Create a .env file with the following content: DATABASE_URL=postgresql+asyncpg://maxim:my_secret_password@postgresql_service:5432/grpc_database_max

6. Build and Start Docker Containers:
make containers (docker-compose up --build -d)

7. Run Alembic Migrations:
alembic upgrade head
