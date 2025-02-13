import React from 'react'
import { useEffect, useState } from 'react'
import { useQuery, gql } from '@apollo/client'
import { GET_USER } from '../GraphQL/Queries'

const GetUser = () => {

    const { error, loading, data} = useQuery(GET_USER, {
        variables: {
            userId: 1
        }
    })
    const [user, setUser] = useState('')

    useEffect(() => {
        if (data) {
        setUser(data.userDetails)
        }
    }, [data])

    return (
        <div>
            <h1>{user.username}</h1>
            <h2>{user.email}</h2>
        </div>
    )
}

export default GetUser