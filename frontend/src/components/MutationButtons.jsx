import React from 'react'
import CardButton from './CardButton'

const MutationButtons = () => {
    return (
        <div className='w-full'>
            <h1 className='mb-5'>Mutations</h1>
            <div className='flex flex-wrap gap-4'>
                <CardButton title="Create User" linkName="Create" linkTo="/create-user" />
                <CardButton title="Update Password" linkName="Update Password" linkTo="/update-password" />
                <CardButton title="Delete User" linkName="Delete" linkTo="/delete-user" />
                <CardButton title="Add Subscription" linkName="Add" linkTo='/' />
                <CardButton title="Activate Subscription" linkName="Activate" linkTo="/" />
                <CardButton title="Extend Subscription" linkName="Extend" linkTo="/" />
                <CardButton title="Deactivate Subscription" linkName="Deactivate" linkTo="/" />
                <CardButton title="Delete Subscription" linkName="Delete" linkTo="/" />

            </div>
        </div>
    )
}

export default MutationButtons