grpc:
	@python -m grpc_tools.protoc -I=protos --python_out=user_service/grpc/generated --grpc_python_out=user_service/grpc/generated protos/user.proto
	@python -m grpc_tools.protoc -I=protos --python_out=subscription_service/grpc/generated --grpc_python_out=subscription_service/grpc/generated protos/subscription.proto
	@echo "gRPC files generated successfully."

install:
	@pip install -r requirements.txt

run:
	@python main.py

stop:
	@/bin/sh Docker/clear_docker_data.sh

start:
	@docker-compose -f Docker/docker-compose.yml up