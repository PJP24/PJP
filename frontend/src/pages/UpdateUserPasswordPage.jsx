import React from 'react'
import { useState } from 'react'
import UpdatePasswordForm from '../components/UpdatePasswordForm';
import UserResponse from '../components/UserResponse';

const UpdateUserPasswordPage = () => {

  const [showResponse, setShowResponse] = useState(false);
  const [response, setResponse] = useState(null);

  return (
      <div>
          <UpdatePasswordForm setShowResponse={setShowResponse} setResponse={setResponse} />
          
          {showResponse && response && <UserResponse response={response} />}
      </div>
  );
};

export default UpdateUserPasswordPage