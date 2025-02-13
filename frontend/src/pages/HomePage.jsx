import React from 'react'
import Hero from '../components/Hero'
import QueryButtons from '../components/QueryButtons'
import MutationButtons from '../components/MutationButtons'

const HomePage = () => {
    return (
        <>
            <Hero />
            <div className='flex flex-col gap-4 ml-5'> 
            <QueryButtons />
            < MutationButtons />
            </div>
        </>
    )
}

export default HomePage