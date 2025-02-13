import React from 'react';

const QueryButtons = () => {
  return (
    <div className="w-full">
      <h1 className="mb-5">Queries</h1>
      <div className="flex flex-wrap gap-4">
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 mb-2">
          <a href="#">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              Get User Details
            </h5>
          </a>
          <button
            href="#"
            className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-700 rounded-lg hover:bg-indigo-400"
          >
            User Details
          </button>
        </div>
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 mb-2">
          <a href="/all-subscriptions">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              Get All Subscriptions
            </h5>
          </a>
          <button
            href="#"
            className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-700 rounded-lg hover:bg-indigo-400"
          >
            Subscriptions
          </button>
        </div>
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 mb-2">
          <a href="/opt-out-policy">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              Opt Out Policy
            </h5>
          </a>
          <button
            href="#"
            className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-700 rounded-lg hover:bg-indigo-400"
          >
            Policy
          </button>
        </div>
      </div>
    </div>
  );
};

export default QueryButtons;
