import React from 'react';
import { DELETE_USER } from '../GraphQL/Mutations';
import GenericUserForm from './GenericUserForm';

const DeleteUserForm = ({ setShowResponse, setResponse }) => {
    const fields = [
        { name: 'userId', label: 'User ID', type: 'number', min: 1 },
      ];
    
      return (
        <GenericUserForm
          title="Delete User"
          mutation={DELETE_USER}
          mutationVariables="deleteUser"
          successMessage="User deleted successfully."
          buttonText="Delete"
          setResponse={setResponse}
          setShowResponse={setShowResponse}
          fields={fields}
        />
      );
    };
export default DeleteUserForm;
