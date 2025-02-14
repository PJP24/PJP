import { gql } from "@apollo/client";

export const CREATE_SUBSCRIPTION = gql`
  mutation AddSubscription($email: String!, $subscriptionType: String!) {
    addSubscription(email: $email, subscriptionType: $subscriptionType) {
      resultInfo
    }
  }
`;
