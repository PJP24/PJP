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
      subscriptionType
    }
  }
}
`