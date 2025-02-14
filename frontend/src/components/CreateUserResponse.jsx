import React from 'react';

const CreateUserResponse = ({user}) => {
  return (
    <div className="flex justify-center items-center mt-20">
      <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Created User</h5>
        
        <p className="text-gray-700 dark:text-gray-400"><strong>Message:</strong> {user.message}</p>
        <p className="text-gray-700 dark:text-gray-400"><strong>Username:</strong> {user.user ? user.user.username : 'None'}</p>
        <p className="text-gray-700 dark:text-gray-400"><strong>Email:</strong> {user.user ? user.user.email :'None'}</p>
        <p className="text-gray-700 dark:text-gray-400"><strong>Id:</strong> {user.user ? user.user.id : 'None'}</p>
</div>
</div>
  );
};

export default CreateUserResponse;
