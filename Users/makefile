.PHONY: init protos server client

init:
	@/bin/sh init.sh

protos:
	python \
		-m grpc_tools.protoc \
		-I./proto_files \
		--python_out=./src/grpc/generated \
		--grpc_python_out=./src/grpc/generated \
		proto_files/user.proto

server:
	python main.py

client:
	python client.py