import React, { useEffect } from 'react';
import { useQuery, gql } from "@apollo/client";
import { OPT_OUT_POLICY } from "../GraphQL/Queries";

const OptOutPolicy = () => {
    const { data } = useQuery(OPT_OUT_POLICY);

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

export default OptOutPolicy;
