###Terminal Commands to Run Subscriptions Service

## 1. Navigate to Subscriptions Directory:
```bash
cd Subscriptions
```

2. Add .env File:
Create a .env file with the following content: DATABASE_URL=postgresql+asyncpg://maxim:my_secret_password@postgresql_service:5432/grpc_database_max

3. Build and Start Docker Containers:
make containers (docker-compose up --build -d)

4. Run Alembic Migrations:
alembic upgrade head

5. Run clien.py
make client