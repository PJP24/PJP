import React from 'react'
import { Link } from 'react-router-dom'

const CardButton = ({ title, linkName, linkTo }) => {
    return (
        <div className="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 mb-2">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{title}</h5>
            {/* <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Provide the user Id</p> */}
            <Link to={linkTo} className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-indigo-700 rounded-lg hover:bg-indigo-400">
                {linkName}
            </Link>
        </div>
    )
}

export default CardButton