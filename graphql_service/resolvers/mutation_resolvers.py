import httpx


async def fetch_data(url: str, method: str = "GET", data: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            elif method == "PATCH":
                response = await client.patch(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            else:
                raise ValueError("Unsupported HTTP method")
            return response.json()
        except Exception as e:
            print(f"Exception in fetch_data: {e}")
            return None


async def add_user(username: str, email: str, password: str):
    from graphql_service.graphql_app import AddUserResponse, User

    user_data = {"username": username, "email": email, "password": password}
    response_data = await fetch_data("http://localhost:5001/add_user", method="POST", data=user_data)

    if not response_data or response_data.get("status") == "error":
        return AddUserResponse(
            status="error", message=response_data.get("message", "Error occurred"), user=None
        )
    return AddUserResponse(
        status="success",
        message=response_data.get("message", "Success"),
        user=User(username=response_data.get("username"), email=response_data.get("email")),
    )


async def update_user_password(user_id: int, old_password: str, new_password: str):
    from graphql_service.graphql_app import UpdateUserResponse

    passwords = {"old_password": old_password, "new_password": new_password}
    response_data = await fetch_data(f"http://localhost:5001/update_password/{user_id}", method="PATCH", data=passwords)

    if not response_data or response_data.get("status") == "error":
        return UpdateUserResponse(
            status="error", message=response_data.get("message", "Error occurred")
        )
    return UpdateUserResponse(
        status="success", message=response_data.get("message", "Success")
    )


async def delete_user(user_id: int):
    from graphql_service.graphql_app import DeleteUserResponse

    response_data = await fetch_data(f"http://localhost:5001/delete_user/{user_id}", method="DELETE")

    if not response_data or response_data.get("status") == "error":
        return DeleteUserResponse(
            status="error", message=response_data.get("message", "Error occurred")
        )
    return DeleteUserResponse(
        status="success", message=response_data.get("message", "Success")
    )


async def add_subscription_resolver(email: str, subscription_type: str):
    from graphql_service.graphql_app import AddSubscriptionResponse

    subscription_data = {"email": email, "subscription_type": subscription_type}
    result_info = await fetch_data("http://localhost:5001/add_subscriptions", method="POST", data=subscription_data)

    if not result_info or "message" not in result_info:
        return AddSubscriptionResponse(result_info="Unknown result")
    return AddSubscriptionResponse(result_info=result_info["message"])


async def change_subscription_resolver(email: str, subscription_type: str):
    from graphql_service.graphql_app import UpdateSubscriptionResponse

    subscription_data = {"email": email, "subscription_type": subscription_type}
    result_info = await fetch_data("http://localhost:5001/change_subscriptions", method="PUT", data=subscription_data)

    if not result_info or "message" not in result_info:
        return UpdateSubscriptionResponse(result_info="Unknown result")
    return UpdateSubscriptionResponse(result_info=result_info["message"])


async def delete_subscription_resolver(email: str):
    from graphql_service.graphql_app import DeleteSubscriptionResponse

    result_info = await fetch_data(f"http://localhost:5001/delete_subscriptions/{email}", method="DELETE")

    if not result_info or "message" not in result_info:
        return DeleteSubscriptionResponse(result_info="Unknown result")
    return DeleteSubscriptionResponse(result_info=result_info["message"])


async def activate_subscription_resolver(email: str):
    from graphql_service.graphql_app import ActivateSubscriptionResponse

    result_info = await fetch_data(f"http://localhost:5001/activate_subscriptions/{email}/activate", method="POST")

    if not result_info or "message" not in result_info:
        return ActivateSubscriptionResponse(result_info="Unknown result")
    return ActivateSubscriptionResponse(result_info=result_info["message"])


async def deactivate_subscription_resolver(email: str):
    from graphql_service.graphql_app import DeactivateSubscriptionResponse

    result_info = await fetch_data(f"http://localhost:5001/deactivate_subscriptions/{email}/deactivate", method="POST")

    if not result_info or "message" not in result_info:
        return DeactivateSubscriptionResponse(result_info="Unknown result")
    return DeactivateSubscriptionResponse(result_info=result_info["message"])
