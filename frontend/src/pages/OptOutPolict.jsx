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
        <div className="p-4 bg-gray-100 rounded-lg shadow-md">
            <h2 className="text-lg font-semibold text-gray-800">Opt-Out Policy</h2>
            {data?.optOutPolicy?.policy ? (
                <p className="mt-2 p-2 bg-white border rounded text-gray-700 text-sm">
                    {data.optOutPolicy.policy}
                </p>
            ) : (
                <p className="mt-2 text-gray-500">No policy available.</p>
            )}
        </div>
    );
};

export default OptOutPolicy;
