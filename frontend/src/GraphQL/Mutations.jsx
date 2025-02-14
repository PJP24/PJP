import { gql } from "@apollo/client";

export const CREATE_SUBSCRIPTION = gql`
  mutation AddSubscription($email: String!, $subscriptionType: String!) {
    addSubscription(email: $email, subscriptionType: $subscriptionType) {
      resultInfo
    }
  }
`;

export const DELETE_SUBSCRIPTION = gql`
  mutation MyMutation($email: String!) {
    deleteSubscription(email: $email) {
      resultInfo
    }
  }
`;

export const ACTIVATE_SUBSCRIPTION = gql`
  mutation ActivateSubscription($amount: Int!, $email: String!) {
    activateSubscription(amount: $amount, email: $email) {
      resultInfo
    }
  }
`;

export const DEACTIVATE_SUBSCRIPTION = gql`
  mutation DeactivateSubscription($email: String!) {
    deactivateSubscription(email: $email) {
      resultInfo
    }
  }
`;