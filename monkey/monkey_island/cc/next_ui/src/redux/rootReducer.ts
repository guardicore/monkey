import { combineReducers } from 'redux';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import authenticationTimerSlice from '@/redux/features/api/authentication/authenticationTimerSlice';

const rootReducer = combineReducers({
    [islandApiSlice.reducerPath]: islandApiSlice.reducer,
    authenticationTimer: authenticationTimerSlice
});

export default rootReducer;
