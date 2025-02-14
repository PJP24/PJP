import {gql} from "@apollo/client"

export const GET_USER = gql `
    query GetUser($userId: Int!) {
  userDetails(userId: $userId) {
    email
    username
    subscription {
      subscriptionEndDate
      subscriptionId
      subscriptionIsActive
    }
  }
}
`

export const LOAD_SUBSCRIPTIONS = gql`
    query MyQuery {
        allSubscriptions {
            amount
            endDate
            id
            isActive
            subscriptionType
            userId
        }
    }
`;

export const OPT_OUT_POLICY = gql`
  query MyQuery {
    optOutPolicy {
      policy
    }
  }
`;
