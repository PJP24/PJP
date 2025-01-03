REPO_ROOT = $(shell git rev-parse --show-toplevel)
PROTO_ROOT = $(REPO_ROOT)/protos
ORCHESTRATOR_OUT = $(REPO_ROOT)/Orchestrator_monolith/src/orchestrator/generated


containers:
	docker-compose up --build -d

all:
	@mkdir -p $(ORCHESTRATOR_OUT)
	@python -m grpc_tools.protoc \
		-I=$(PROTO_ROOT) \
		--grpc_python_out=$(ORCHESTRATOR_OUT)\
		--python_out=$(ORCHESTRATOR_OUT) \
		$(PROTO_ROOT)/*.proto

generate_all_protos_in_subscriptions:
	mkdir -p Subscriptions/src/grpc/generated && python -m grpc_tools.protoc --proto_path=protos --python_out=Subscriptions/src/grpc/generated --grpc_python_out=Subscriptions/src/grpc/generated protos/subscription.proto

clear_docker_data:
	@/bin/sh clear_docker_data.sh
