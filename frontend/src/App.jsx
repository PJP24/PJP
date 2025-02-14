import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  HttpLink,
  from
} from '@apollo/client'

import { onError } from '@apollo/client/link/error'

import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from 'react-router-dom'
import HomePage from './pages/HomePage';
import MainLayout from './layouts/MainLayout';
import NotFoundPage from './pages/NotFoundPage';
import AllSubscriptions from './pages/AllSubscriptions';
import OptOutPolicy from './pages/OptOutPolict';
import AddSubscription from './pages/AddSubscription';
import DeleteSubscription from './pages/DeleteSubscription';

const errorLink = onError(({ graphqlErrors }) => {
  if (graphqlErrors) {
    graphqlErrors.map(({ message }) => {
      alert(`GraphQL error ${message}`)
    });
  }
});

const link = from([
  errorLink,
  new HttpLink({ uri: "http://localhost:5001" })
])

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: link
})

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path='/' element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path='*' element={<NotFoundPage />} />
        <Route path='/all-subscriptions' element={<AllSubscriptions />} />
        <Route path='/opt-out-policy' element={<OptOutPolicy />} />
        <Route path='/add-subscription' element={<AddSubscription />} />
        <Route path='/delete-subscription' element={<DeleteSubscription />} />
      </Route>
    )
  );

  return (
    <ApolloProvider client={client}> 
      <RouterProvider router={router} />
    </ApolloProvider>
)
}

export default App
