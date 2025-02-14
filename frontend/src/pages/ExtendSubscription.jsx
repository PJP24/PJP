import React, { useState } from 'react';
import { useMutation } from '@apollo/client';
import { EXTEND_SUBSCRIPTION } from '../GraphQL/Mutations';

const ExtendSubscription = () => {
  const [email, setEmail] = useState('');
  const [amount, setAmount] = useState(20); // Default amount set to 20
  const [extendSubscription, { loading, error, data }] = useMutation(EXTEND_SUBSCRIPTION);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await extendSubscription({ variables: { email, amount } });
    } catch (err) {
      console.error("Error extending subscription:", err);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Extend Subscription</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email:</label>
          <input
            type="email"
            id="email"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700">Amount:</label>
          <input
            type="number"
            id="amount"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={amount}
            onChange={(e) => setAmount(parseInt(e.target.value))}
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className={`w-full px-4 py-2 font-semibold text-white bg-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? 'Extending...' : 'Extend Subscription'}
        </button>
      </form>

      {error && <p className="mt-4 text-red-500">{error.message}</p>}
      {data && <p className="mt-4 text-green-500">Subscription extended successfully! {data.extendSubscription.resultInfo}</p>}
    </div>
  );
};

export default ExtendSubscription;
