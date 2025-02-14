import React, { useState } from 'react';
import { useMutation } from "@apollo/client";
import { DELETE_SUBSCRIPTION } from '../GraphQL/Mutations';

const DeleteSubscription = () => {
    const [email, setEmail] = useState("");
    const [result, setResult] = useState(null);

    const [deleteSubscription, { error, loading }] = useMutation(DELETE_SUBSCRIPTION);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await deleteSubscription({
            variables: { email }
        });

        if (response.data) {
            setResult(response.data.deleteSubscription.resultInfo);
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white shadow-md rounded-lg p-6 mt-10">
            <h2 className="text-2xl font-bold text-center mb-4">Delete Subscription</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-gray-700 font-medium">Email:</label>
                    <input 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <button 
                    type="submit" 
                    disabled={loading}
                    className="w-full bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition duration-300 disabled:bg-gray-400"
                >
                    {loading ? "Deleting..." : "Delete Subscription"}
                </button>
            </form>

            {error && <p className="text-red-500 mt-4 text-center">Error: {error.message}</p>}
            {result && <p className="text-green-500 mt-4 text-center">Result: {result}</p>}
        </div>
    );
};

export default DeleteSubscription;
