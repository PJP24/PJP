import React from 'react';
import { UPDATE_PASSWORD } from '../GraphQL/Mutations';
import GenericUserForm from './GenericUserForm';

const UpdatePasswordForm = ({ setResponse, setShowResponse }) => {
  const fields = [
    { name: 'userId', label: 'User ID', type: 'number', min: 1 },
    { name: 'oldPassword', label: 'Old Password', type: 'text' },
    { name: 'newPassword', label: 'New Password', type: 'text' },
  ];

  return (
    <GenericUserForm
      title="Update Password"
      mutation={UPDATE_PASSWORD}
      mutationVariables="updatePassword"
      successMessage="Password updated successfully."
      buttonText="Update"
      setResponse={setResponse}
      setShowResponse={setShowResponse}
      fields={fields}
    />
  );
};

export default UpdatePasswordForm;
