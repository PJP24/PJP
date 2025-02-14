import { gql } from "@apollo/client"

export const CREATE_USER = gql`

    mutation createUser(
        $email: String! 
        $password: String!
        $username: String!
        ) {
        createUser(
            email: $email 
            password: $password
            username: $username
            ) {
                status
                message
                user {
                    email
                    id
                    username
                }
            }
    }
`

export const DELETE_USER = gql`

    mutation deleteUser(
        $userId: Int!    
    ) {
        deleteUser(
        userId: $userId
    ) {
        message
        status
        }    
    }

`

export const UPDATE_PASSWORD = gql`
    mutation updatePassword(
        $userId: Int!
        $oldPassword: String!
        $newPassword: String!
    ) {
        updatePassword(
            userId: $userId
            oldPassword: $oldPassword
            newPassword: $newPassword
        ) {
            message
            status    
        }         
    }
`


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

export const EXTEND_SUBSCRIPTION = gql`
  mutation MyMutation($amount: Int!, $email: String!) {
    extendSubscription(amount: $amount, email: $email) {
      resultInfo
    }
  }
`;
