'use client'
import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'

// Define a service using a base URL and expected endpoints
export const islandApi = createApi({
    reducerPath: 'islandApi',
    baseQuery: fetchBaseQuery({
        baseUrl: '/api',
        prepareHeaders: (headers, {getState}) => {
            headers.set('Content-Type', 'application/json')
            headers.set('Authentication-Token', localStorage.getItem('authentication_token'));
            return headers
        }
    }),
    endpoints: (builder) => ({
        getAllMachines: builder.query({query: () => '/machines'})
    })
})

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const {useGetAllMachinesQuery} = islandApi
