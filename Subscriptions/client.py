import grpc
from src.grpc.generated.subscription_pb2 import (
    CreateSubscriptionRequest, 
    GetSubscriptionsRequest, 
    ChangeSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest, 
    OptOutPolicyRequest,
    DeactivateSubscriptionRequest,
    GetSubscriptionsDynamoDBRequest,
    CreateSubscriptionDynamoDBRequest,
    DeleteSubscriptionDynamoDBRequest,
    ChangeSubscriptionTypeDynamoDBRequest,
)
from src.grpc.generated.subscription_pb2_grpc import SubscriptionServiceStub

class SubscriptionClient:
    def __init__(self, server_address='localhost:50051'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = SubscriptionServiceStub(self.channel)

    def create_subscription(self):
        email = input("Enter email: ")
        subscription_type = input("Enter subscription type (monthly/yearly): ")

        request = CreateSubscriptionRequest(email=email, subscription_type=subscription_type)
        response = self.stub.CreateSubscription(request)
        
        print(response.message)

    def get_subscriptions(self):
        request = GetSubscriptionsRequest()
        response = self.stub.GetSubscriptions(request)
        
        if len(response.subscriptions) > 0:
            print("\nCurrent Subscriptions:")
            for sub in response.subscriptions:
                print(f"Email: {sub.email}, Type: {sub.subscription_type}, Is active: {sub.is_active}")
        else:
            print("No subscriptions found.")

    def change_subscription(self):
        email = input("Enter email to change subscription: ")
        subscription_type = input("Enter new subscription type (monthly/yearly): ")

        request = ChangeSubscriptionRequest(email=email, subscription_type=subscription_type)
        response = self.stub.ChangeSubscription(request)

        print(response.message)

    def delete_subscription(self):
        email = input("Enter email to delete subscription: ")

        request = DeleteSubscriptionRequest(email=email)
        response = self.stub.DeleteSubscription(request)

        print(response.message)

    def activate_subscription(self):
        email = input("Enter email to activate subscription: ")

        request = ActivateSubscriptionRequest(email=email)
        response = self.stub.ActivateSubscription(request)

        print(response.message)
    
    def opt_out_policy(self):
        request = OptOutPolicyRequest()
        response = self.stub.OptOutPolicy(request)

        print(response.policy)

    def deactivate_subscription(self):
        email = input("Enter email to deactivate subscription: ")

        request = DeactivateSubscriptionRequest(email=email)
        response = self.stub.DeactivateSubscription(request)

        print(response.message)
    
    def get_subscriptions_dynamodb(self):
        request = GetSubscriptionsDynamoDBRequest()
        response = self.stub.GetSubscriptionsDynamoDB(request)

        if len(response.subscriptions) > 0:
            print("\nCurrent Subscriptions:")
            for sub in response.subscriptions:
                print(f"Email: {sub.email}, Type: {sub.subscription_type}, Is active: {sub.is_active}")
        else:
            print("No subscriptions found.")
        
    def create_subscription_dynamodb(self):
        email = input("Enter email: ")
        subscription_type = input("Enter subscription type (monthly/yearly): ")
        is_active_str = input("Enter activity status (True/False): ")

        is_active = is_active_str.lower() == 'true'

        request = CreateSubscriptionDynamoDBRequest(email=email, subscription_type=subscription_type, is_active=is_active)
        response = self.stub.CreateSubscriptionDynamoDB(request)
        
        print(response.message)

    def delete_subscription_dynamodb(self):
        email = input("Enter email to delete subscription from DynamoDB: ")

        request = DeleteSubscriptionDynamoDBRequest(email=email)
        response = self.stub.DeleteSubscriptionDynamoDB(request)

        print(response.message)

    def change_subscription_dynamodb(self):
        email = input("Enter email to change subscription in DynamoDB: ")
        new_subscription_type = input("Enter new subscription type (monthly/yearly): ")

        request = ChangeSubscriptionTypeDynamoDBRequest(email=email, new_subscription_type=new_subscription_type)
        response = self.stub.ChangeSubscriptionTypeDynamoDB(request)

        print(response.message)

    def main(self):
        while True:
            print("\nChoose an option:")
            print("1. Create a new subscription")
            print("2. View all subscriptions")
            print("3. Change existing subscription")
            print("4. Delete existing subscription")
            print("5. Activate subscription")
            print("6. Opt-Out Policy")
            print("7. Deactivate subscription")
            print("8. View all subscriptions (DynamoDB)")
            print("9. Create new subscription (DynamoDB)")
            print("10. Delete subscription (DynamoDB)")
            print("11. Change subscription type (DynamoDB)")  # New option
            print("Type 'exit' to return to the terminal.\n")

            choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10/11/exit): ")

            if choice == '1':
                self.create_subscription()
            elif choice == '2':
                self.get_subscriptions()
            elif choice == '3':
                self.change_subscription()
            elif choice == '4':
                self.delete_subscription()
            elif choice == '5':
                self.activate_subscription()
            elif choice == '6':
                self.opt_out_policy()
            elif choice == '7':
                self.deactivate_subscription()
            elif choice == '8':
                self.get_subscriptions_dynamodb()
            elif choice == '9':
                self.create_subscription_dynamodb()
            elif choice == '10':
                self.delete_subscription_dynamodb()
            elif choice == '11':
                self.change_subscription_dynamodb()
            elif choice == 'exit':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 or exit.\n")

if __name__ == '__main__':
    client = SubscriptionClient()
    client.main()
