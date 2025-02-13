import React, {useEffect} from 'react';
import { useQuery, gql } from "@apollo/client";
import { LOAD_SUBSCRIPTIONS } from "../GraphQL/Queries"



const GetSubscriptions = () => {

    const { error, loading, data } = useQuery(LOAD_SUBSCRIPTIONS);

    useEffect (() => {
        console.log(data)
    }, [data])

    return (
        <div></div>
    )
}

export default GetSubscriptions