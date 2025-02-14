import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { CREATE_USER } from '../GraphQL/Mutations';
import { toast } from 'react-toastify';

const CreateUserForm = ({ setShowCreatedUser, setUser }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [createUser, { data, error, loading }] = useMutation(CREATE_USER);

     useEffect(() => {
            if (data) {
                setUser(data.createUser);
                setShowCreatedUser(true);
            if (data.createUser.status === 'success') {
                toast.success('User created successfully.');
            }
            }
        }, [data, setUser]);

    const AddUser = (e) => {
        e.preventDefault();
        createUser({
            variables: {
                username: username,
                email: email,
                password: password,
            },
        });

        setUsername('');
        setPassword('');
        setEmail('');
    };

    
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div className="flex justify-center mt-10">
            <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
                <Link to="/" className="px-3 py-1 bg-red-500 rounded-md text-white text-sm shadow-md mb-3 inline-block">
                    Go Back
                </Link>
                <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center">Create User</h5>

                <form onSubmit={AddUser}>
                    <div className="mb-3">
                        <label htmlFor="username" className="text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                        <input
                            type="text"
                            name="username"
                            id="username"
                            className="block w-full px-3 py-2 text-sm border rounded-md bg-white dark:bg-white-700 text-gray-900 dark:text-black focus:ring-2 focus:ring-indigo-500"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="email" className="text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
                        <input
                            type="email"
                            name="email"
                            id="email"
                            className="block w-full px-3 py-2 text-sm border rounded-md bg-white dark:bg-white-700 text-gray-900 dark:text-black focus:ring-2 focus:ring-indigo-500"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            className="block w-full px-3 py-2 text-sm border rounded-md bg-white dark:bg-white-700 text-gray-900 dark:text-black focus:ring-2 focus:ring-indigo-500"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full px-3 py-2 text-sm font-medium text-white bg-emerald-500 rounded-md hover:bg-emerald-600 shadow-md">
                        Create
                    </button>
                </form>
            </div>
        </div>
    );
};

export default CreateUserForm;
