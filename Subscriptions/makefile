.PHONY: protos server client init clear_docker_data containers

protos:
	python \
		-m grpc_tools.protoc \
		-I./proto_files \
		--python_out=./src/grpc/generated \
		--grpc_python_out=./src/grpc/generated \
		proto_files/subscription.proto

server:
	python main.py

client:
	python client.py

init:
	@/bin/sh scripts/init.sh

clear_docker_data:
	@/bin/sh scripts/clear_docker_data.sh

containers:
	cd docker && docker-compose up --build -d