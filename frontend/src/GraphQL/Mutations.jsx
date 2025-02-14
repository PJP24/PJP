import { gql } from "@apollo/client"

export const CREATE_USER = gql`

    mutation createUser(
        $email: String! 
        $password: String!
        $username: String!
        ) {
        createUser(
            email: $email 
            password: $password
            username: $username
            ) {
                status
                message
                user {
                    email
                    id
                    username
                }
            }
    }
`

export const DELETE_USER = gql`

    mutation deleteUser(
        $userId: Int!    
    ) {
        deleteUser(
        userId: $userId
    ) {
        message
        status
        }    
    }

`

export const UPDATE_PASSWORD = gql`
    mutation updatePassword(
        $userId: Int!
        $oldPassword: String!
        $newPassword: String!
    ) {
        updatePassword(
            userId: $userId
            oldPassword: $oldPassword
            newPassword: $newPassword
        ) {
            message
            status    
        }         
    }
`