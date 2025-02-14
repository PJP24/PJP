import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLazyQuery } from '@apollo/client';
import { GET_USER } from '../GraphQL/Queries';

const UserQueryForm = ({ setShowUserDetails, setUser }) => {
    const [userId, setUserId] = useState('');
    const [getUser, { error, loading, data }] = useLazyQuery(GET_USER);

    useEffect(() => {
        if (data) {
            setUser(data.userDetails);
        }
    }, [data, setUser]);

    const searchUser = (e) => {
        e.preventDefault();
        if (userId) {
            getUser({ variables: { userId } });
            setShowUserDetails(true);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div className="flex justify-center mt-10">
            <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
                <Link to="/" className="px-3 py-1 bg-red-500 rounded-md text-white text-sm shadow-md mb-3 inline-block">
                    Go Back
                </Link>
                <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center">Search User</h5>

                <form onSubmit={searchUser}>
                    <div className="mb-3">
                        <label htmlFor="userId" className="text-sm font-medium text-gray-700 dark:text-gray-300">User ID</label>
                        <input
                            type="number"
                            name="userId"
                            id="userId"
                            min = '1'
                            className="block w-full px-3 py-2 text-sm border rounded-md bg-white dark:bg-white-700 text-gray-900 dark:text-black focus:ring-2 focus:ring-indigo-500"
                            required
                            value={userId}
                            onChange={(e) => setUserId(e.target.value ? parseInt(e.target.value) : '')}
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full px-3 py-2 text-sm font-medium text-white bg-emerald-500 rounded-md hover:bg-emerald-600 shadow-md">
                        Search
                    </button>
                </form>

            </div>
        </div>
    );
};

export default UserQueryForm;
