import { combineReducers } from 'redux';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import authenticationTimerSlice from '@/redux/features/api/authentication/authenticationTimerSlice';
import pluginInstallationStatusSlice from '@/redux/features/api/agentPlugins/pluginInstallationStatusSlice';

const rootReducer = combineReducers({
    [islandApiSlice.reducerPath]: islandApiSlice.reducer,
    [pluginInstallationStatusSlice.name]: pluginInstallationStatusSlice.reducer,
    authenticationTimer: authenticationTimerSlice
});

export default rootReducer;
