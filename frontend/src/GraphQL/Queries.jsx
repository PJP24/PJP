import { gql } from "@apollo/client";


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
`