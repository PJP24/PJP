import React from 'react';

const UserResponse = ({response}) => {
  return (
    <div className="flex justify-center items-center mt-20">
      <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Response</h5>
        
        <p className="text-gray-700 dark:text-gray-400"><strong>Message:</strong> {response.message}</p>
</div>
</div>
  );
};

export default UserResponse;
