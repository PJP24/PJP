import React, { useEffect } from 'react';
import { useQuery, gql } from "@apollo/client";
import { LOAD_SUBSCRIPTIONS } from "../GraphQL/Queries";

const GetSubscriptions = () => {
    const { data } = useQuery(LOAD_SUBSCRIPTIONS);

    useEffect(() => {
        if (data) {
            console.log(data);
        }
    }, [data]);

    return (
        <div>
            Data: {JSON.stringify(data)}
        </div>
    );
};

export default GetSubscriptions;
