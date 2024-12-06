import grpc
from src.grpc.generated.subscription_pb2 import (
    CreateSubscriptionRequest, 
    GetSubscriptionsRequest, 
    ChangeSubscriptionRequest,
    DeleteSubscriptionRequest,
    ActivateSubscriptionRequest, 
    DeactivateSubscriptionRequest,
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

        if response.subscriptions:
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

    def deactivate_subscription(self):
        email = input("Enter email to deactivate subscription: ")

        request = DeactivateSubscriptionRequest(email=email)
        response = self.stub.DeactivateSubscription(request)

        print(response.message)

    def main(self):
        while True:
            print("\nChoose an option:")
            print("1. Create a new subscription")
            print("2. View all subscriptions")
            print("3. Change existing subscription")
            print("4. Delete existing subscription")
            print("5. Activate subscription")
            print("6. Deactivate subscription")
            print("7. Exit\n")

            choice = input("Enter your choice (1/2/3/4/5/6/7): ")

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
                self.deactivate_subscription()
            elif choice == '7':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose 1, 2, 3, 4, 5, 6 or 7.\n")

if __name__ == '__main__':
    client = SubscriptionClient()
    client.main()
