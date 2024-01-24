import { combineReducers } from 'redux';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import themeSliceReducer from './features/theme/theme.slice';
import authenticationTimerSlice from '@/redux/features/api/authentication/authenticationTimerSlice';

const rootReducer = combineReducers({
    [islandApiSlice.reducerPath]: islandApiSlice.reducer,
    authenticationTimer: authenticationTimerSlice,
    theme: themeSliceReducer
});

export default rootReducer;
