Terminal commands to run Subscriptions service:


cd Subscriptions

add .env with: DATABASE_URL=postgresql+asyncpg://maxim:my_secret_password@postgresql_service:5432/grpc_database_max

make containers (docker-compose up --build -d)

make client



If needed:

Create the db from PGAdmin

Login to PDAdmin using those credentials:
email: admin@admin.com
password: admin_password


Create a server:
Use any server name (for example: Server 1)

Host name/address: postgresql_service
Port: 5432
Username: maxim
Password: my_secret_password
