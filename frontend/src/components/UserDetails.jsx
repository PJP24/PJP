import React from 'react';

const UserDetails = ({user}) => {
  return (
    <div className="flex justify-center items-center mt-20">
      <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">User Details</h5>
        
        <p className="text-gray-700 dark:text-gray-400"><strong>Username:</strong> {user.username}</p>
        <p className="text-gray-700 dark:text-gray-400"><strong>Email:</strong> {user.email}</p>

        <div className="mt-4 border-t border-gray-300 pt-4">
          <h6 className="text-lg font-semibold text-gray-900 dark:text-white">Subscription Info</h6>
          {/* TODO - FIX THE SUBSCRIPTION TYPE PROBLEM */}
          {/* <p className="text-gray-700 dark:text-gray-400"><strong>Type:</strong> {user.subscription ? user.subscription.subscription_type : 'None'}</p> */}
          <p className="text-gray-700 dark:text-gray-400"><strong>ID:</strong> {user.subscription ? user.subscription.subscriptionId : 'None'}</p>
          <p className="text-gray-700 dark:text-gray-400"><strong>Active:</strong> {user.subscription ? user.subscription.subscriptionIsActive : 'None'}</p>
          <p className="text-gray-700 dark:text-gray-400"><strong>End Date:</strong> {user.subscription ? user.subscription.subscriptionEndDate : 'None'}</p>
        </div>
      </div>
    </div>
  );
};

export default UserDetails;
