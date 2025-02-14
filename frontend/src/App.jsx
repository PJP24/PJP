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
import UserDetailsPage from './pages/UserDetailsPage';
import CreateUserPage from './pages/CreateUserPage';
import DeleteUserPage from './pages/DeleteUserPage';
import UpdateUserPasswordPage from './pages/UpdateUserPasswordPage';

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
        <Route path='/user-details' element={<UserDetailsPage />} />
        <Route path='/create-user' element={<CreateUserPage />} />
        <Route path='/delete-user' element={<DeleteUserPage />} />
        <Route path='/update-password' element={<UpdateUserPasswordPage />} />
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