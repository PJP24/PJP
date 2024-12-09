.PHONY: tree grpc install run server

tree:
	@tree -L 3 > tree.txt

grpc:
	@python -m grpc_tools.protoc -I=proto --python_out=grpc_gen/generated --grpc_python_out=grpc_gen/generated proto/user.proto

main:
	@python main.py

server:
	@python server.py
