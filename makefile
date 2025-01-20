REPO_ROOT = $(shell git rev-parse --show-toplevel)
PROTO_ROOT = $(REPO_ROOT)/protos
ORCHESTRATOR_OUT = $(REPO_ROOT)/Orchestrator_monolith/src/orchestrator/generated

generate_all_protos_in_orchestrator:
	@mkdir -p $(ORCHESTRATOR_OUT)
	@python -m grpc_tools.protoc \
		-I=$(PROTO_ROOT) \
		--grpc_python_out=$(ORCHESTRATOR_OUT)\
		--python_out=$(ORCHESTRATOR_OUT) \
		$(PROTO_ROOT)/*.proto

generate_all_protos_in_subscriptions:
	python -m grpc_tools.protoc --proto_path=protos --python_out=subscription_service/src/grpc/generated --grpc_python_out=subscription_service/src/grpc/generated protos/subscription.proto

generate_all_protos_in_orchestrator:
	python -m grpc_tools.protoc --proto_path=protos --python_out=Orchestrator_monolith/src/generated --grpc_python_out=Orchestrator_monolith/src/generated protos/subscription.proto

create:
	docker-compose up --build -d

clean-containers:
	@docker ps -a -q | xargs -r docker rm -f

clean-images:
	@docker images -q | xargs -r docker rmi

clean: clean-containers clean-images