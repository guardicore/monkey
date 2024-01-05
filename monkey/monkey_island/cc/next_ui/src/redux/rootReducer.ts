import { combineReducers } from 'redux';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import themeSliceReducer from './features/theme/theme.slice';

const rootReducer = combineReducers({
    [islandApiSlice.reducerPath]: islandApiSlice.reducer,
    theme: themeSliceReducer
});

export default rootReducer;
