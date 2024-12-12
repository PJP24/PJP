grpc:
	@python -m grpc_tools.protoc -I=proto --python_out=grpc_gen/generated --grpc_python_out=grpc_gen/generated proto/user.proto
	@python -m grpc_tools.protoc -I=proto --python_out=grpc_gen/generated --grpc_python_out=grpc_gen/generated proto/subscription.proto

install:
	@pip install -r requirements.txt

test:
	@coverage run --omit="grpc_gen/*,api_services/*" -m unittest discover
	@coverage report

docker_stop:
	@docker-compose down --remove-orphans

docker_start:
	@docker compose up --build