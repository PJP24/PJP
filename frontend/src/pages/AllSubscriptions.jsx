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

    if (!data) return <div>Loading...</div>;

    return (
        <div className="p-4 bg-gray-100 rounded-lg shadow-md">
            <h2 className="text-lg font-semibold text-gray-800">Subscriptions</h2>
            <div className="mt-4">
                {data.allSubscriptions.length === 0 ? (
                    <p>No subscriptions available.</p>
                ) : (
                    data.allSubscriptions.map(subscription => (
                        <div key={subscription.id} className="p-4 mb-4 bg-white border rounded shadow-sm">
                            <h3 className="text-md font-semibold text-gray-700">Subscription ID: {subscription.id}</h3>
                            <p><strong>User ID:</strong> {subscription.userId}</p>
                            <p><strong>Subscription Type:</strong> {subscription.subscriptionType}</p>
                            <p><strong>Active:</strong> {subscription.isActive ? 'Yes' : 'No'}</p>
                            <p><strong>End Date:</strong> {subscription.endDate}</p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default GetSubscriptions;
