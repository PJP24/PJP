import React from 'react'
import UserQueryForm from '../components/UserQueryForm'
import UserDetails from '../components/UserDetails'
import { useState } from 'react'

const UserDetailsPage = () => {

    const [showUserDetails, setShowUserDetails] = useState(false);

    const toggleForm = () => {
        setShowUserDetails((prev) => !prev);
    };

    const [user, setUser] = useState(null)
    return (
        <div>
            <UserQueryForm 
                setShowUserDetails={setShowUserDetails} 
                setUser={setUser} 
            />
             {showUserDetails && user && <UserDetails user={user} />}
        </div>
    )
}

export default UserDetailsPage