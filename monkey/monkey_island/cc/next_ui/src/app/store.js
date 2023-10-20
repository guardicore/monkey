import { configureStore } from '@reduxjs/toolkit'
import machineSlice from '@/features/machineSlice';

export default configureStore({
  reducer: {
    machines: machineSlice
  }
})
