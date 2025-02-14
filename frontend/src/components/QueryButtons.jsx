import React from 'react'
import CardButton from './CardButton'

const QueryButtons = () => {
  return (
    
<div className='w-full'> 
    <h1 className='mb-5'>Queries</h1>
    <div className='flex flex-wrap gap-4'>
    <CardButton title="Get User Details" linkName="User" linkTo="/user-details" />
    <CardButton title="Get All Subscriptions" linkName="Subscriptions" linkTo='/' />
    <CardButton title="Opt Out Policy" linkName="Policy" linkTo="/" />
</div>
</div>
  )
}

export default QueryButtons