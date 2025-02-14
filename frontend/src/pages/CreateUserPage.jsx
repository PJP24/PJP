import React, { useState } from 'react';
import CreateUserForm from '../components/CreateUserForm';
import CreateUserResponse from '../components/CreateUserResponse';

const CreateUserPage = () => {
    const [showCreatedUser, setShowCreatedUser] = useState(false);
    const [user, setUser] = useState(null);

    return (
        <div>
            <CreateUserForm setShowCreatedUser={setShowCreatedUser} setUser={setUser} />
            
            {showCreatedUser && user && <CreateUserResponse user={user} />}
        </div>
    );
};

export default CreateUserPage;
