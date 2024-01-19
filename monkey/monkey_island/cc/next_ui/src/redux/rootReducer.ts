import { combineReducers } from 'redux';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import themeSliceReducer from './features/theme/theme.slice';
import authenticationTimeoutSlice from '@/redux/features/api/authenticationTimerSlice';

const rootReducer = combineReducers({
    [islandApiSlice.reducerPath]: islandApiSlice.reducer,
    authenticationTimeout: authenticationTimeoutSlice,
    theme: themeSliceReducer
});

export default rootReducer;
