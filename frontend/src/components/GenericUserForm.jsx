import React, { useEffect, useState } from 'react'
import { useMutation } from '@apollo/client'
import { Link } from 'react-router-dom';
import {toast} from 'react-toastify'

const GenericUserForm = ({
    title,
    mutation,
    mutationVariables,
    successMessage,
    buttonText,
    setResponse,
    setShowResponse,
    fields
}) => {
    const [formData, setFormData] = useState({});
    const [mutationFunction, {error, loading, data}] = useMutation(mutation)

    useEffect(() => {
        if (data) {
          setResponse(data[mutationVariables]);
          setShowResponse(true);
          if (data[mutationVariables].status === 'success') {
            toast.success(successMessage);
          }
        }
      }, [data, setResponse]);
      

      const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
          ...formData,
          [name]: value,
        });
      };
      
      const handleSubmit = (e) => {
        e.preventDefault();

        const variables = { ...formData };

        fields.forEach((field) => {
            if (field.type === 'number' || field.isInteger) {
                variables[field.name] = parseInt(variables[field.name], 10); 
            }
        });

        mutationFunction({ variables });

        setFormData({});
    };
      
      
      return (
        <div className="flex justify-center mt-10">
          <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-indigo-600 dark:border-gray-700">
            <Link to="/" className="px-3 py-1 bg-red-500 rounded-md text-white text-sm shadow-md mb-3 inline-block">
              Go Back
            </Link>
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center">{title}</h5>
    
            <form onSubmit={handleSubmit}>
              {fields.map((field) => (
                <div className="mb-3" key={field.name}>
                  <label htmlFor={field.name} className="text-sm font-medium text-gray-700 dark:text-gray-300">{field.label}</label>
                  <input
                    type={field.type}
                    name={field.name}
                    id={field.name}
                    min={field.min || ''}
                    className="block w-full px-3 py-2 text-sm border rounded-md bg-white dark:bg-white-700 text-gray-900 dark:text-black focus:ring-2 focus:ring-indigo-500"
                    required
                    value={formData[field.name] || ''}
                    onChange={handleInputChange}
                  />
                </div>
              ))}
    
              <button
                type="submit"
                className="w-full px-3 py-2 text-sm font-medium text-white bg-emerald-500 rounded-md hover:bg-emerald-600 shadow-md">
                {buttonText}
              </button>
            </form>
          </div>
        </div>
      );
    };

export default GenericUserForm