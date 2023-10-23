import { configureStore } from '@reduxjs/toolkit'
import machineSlice from '@/features/machineSlice';
import {islandApi} from '@/fetching/islandApiSlice';

export default configureStore({
  reducer: {
    machines: machineSlice,
    [islandApi.reducerPath]: islandApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(islandApi.middleware),
})
