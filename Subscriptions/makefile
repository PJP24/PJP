.PHONY: protos server client init clear_docker_data containers

init:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

protos:
	python \
		-m grpc_tools.protoc \
		-I./proto_files \
		--python_out=./src/grpc/generated \
		--grpc_python_out=./src/grpc/generated \
		proto_files/subscription.proto

clear_docker_data:
	@/bin/sh scripts/clear_docker_data.sh

containers:
	docker-compose up --build -d


client:
	python client.py