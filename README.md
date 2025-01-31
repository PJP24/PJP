python -m grpc_tools.protoc -I=protos --python_out=subscription_service/src/grpc_services/generated --grpc_python_out=subscription_service/src/grpc_services/generated protos/subscription.proto
python -m grpc_tools.protoc -I=protos --python_out=user_service/src/grpc_services/generated --grpc_python_out=user_service/src/grpc_services/generated protos/user.proto
python -m grpc_tools.protoc -I=protos --python_out=orchestrator_monolith/src/generated --grpc_python_out=orchestrator_monolith/src/generated protos/*.proto

psql -U test -d user_management
SELECT * FROM users;


psql -U user_1 -d grpc_database
SELECT * FROM subscriptions;


psql -U tasks -d tasks_db
SELECT * FROM tasks;