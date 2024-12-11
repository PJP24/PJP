.PHONY: tree grpc install run server

tree:
	@tree -L 3 > tree.txt

grpc:
	@python -m grpc_tools.protoc -I=proto --python_out=grpc_gen/generated --grpc_python_out=grpc_gen/generated proto/user.proto
	@python -m grpc_tools.protoc -I=proto --python_out=grpc_gen/generated --grpc_python_out=grpc_gen/generated proto/subscription.proto

install:
	@pip install -r requirements.txt

api:
	@python main.py

servers:
	@python servers.py

test:
	@coverage run --omit="grpc_gen/*,api_services/*" -m unittest discover
	@coverage report
