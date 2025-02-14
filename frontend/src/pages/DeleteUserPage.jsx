import React from 'react'
import DeleteUserForm from '../components/DeleteUserForm';
import UserResponse from '../components/UserResponse';
import { useState } from 'react'

const DeleteUserPage = () => {
    const [showResponse, setShowResponse] = useState(false);
    const [response, setResponse] = useState(null);

    return (
        <div>
            <DeleteUserForm setShowResponse={setShowResponse} setResponse={setResponse} />
            
            {showResponse && response && <UserResponse response={response} />}
        </div>
    );
};

export default DeleteUserPage