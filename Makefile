grpc:
	@python -m grpc_tools.protoc -I=protos --python_out=user_service/grpc_services/generated --grpc_python_out=user_service/grpc_services/generated protos/user.proto
	@python -m grpc_tools.protoc -I=protos --python_out=subscription_service/grpc_services/generated --grpc_python_out=subscription_service/grpc_services/generated protos/subscription.proto
	@python -m grpc_tools.protoc -I=protos --python_out=orchestrator/generated --grpc_python_out=orchestrator/generated protos/*.proto
	@echo "gRPC files generated successfully."

install:
	@pip install -r requirements.txt

run:
	@python main.py

stop:
	@/bin/sh Docker/clear_docker_data.sh

start:
	@docker-compose -f Docker/docker-compose.yml up