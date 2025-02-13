import "./App.css";
import { ApolloClient, InMemoryCache, ApolloProvider, HttpLink, from } from "@apollo/client";
import { onError } from "@apollo/client/link/error";
import GetSubscriptions from "./components/GetSubscriptions";

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      alert(`GraphQL error: ${message}`);
    });
  }
});

const link = from([
  errorLink,
  new HttpLink({ uri: "http://localhost:5001/graphql" }),
]);

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: link,
});

function App() {
  return (
    <div>
    
      <ApolloProvider client={client}>
        <GetSubscriptions /> 
      </ApolloProvider>

      <h2>Users - Query Actions:</h2>
      <button onClick={() => handleUserQuery('userDetails')}>User Details</button>

      <h2>Users - Mutation Actions:</h2>
      <button onClick={() => handleUserMutation('createUser')}>Create User</button>
      <button onClick={() => handleUserMutation('deleteUser')}>Delete User</button>
      <button onClick={() => handleUserMutation('updatePassword')}>Update Password</button>

      <h2>Subscriptions - Query Actions:</h2>
      <button onClick={() => handleSubscriptionQuery('allSubscriptions')}>All Subscriptions</button>
      <button onClick={() => handleSubscriptionQuery('optOutPolicy')}>Opt-Out Policy</button>

      <h2>Subscriptions - Mutation Actions:</h2>
      <button onClick={() => handleSubscriptionMutation('activateSubscription')}>Activate Subscription</button>
      <button onClick={() => handleSubscriptionMutation('addSubscription')}>Add Subscription</button>
      <button onClick={() => handleSubscriptionMutation('deactivateSubscription')}>Deactivate Subscription</button>
      <button onClick={() => handleSubscriptionMutation('deleteSubscription')}>Delete Subscription</button>
      <button onClick={() => handleSubscriptionMutation('extendSubscription')}>Extend Subscription</button>
    </div>
  );
}

export default App;
