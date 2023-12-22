import { combineReducers } from 'redux';
import { externalApiSlice } from '@/redux/features/api/externalApiSlice';
import { internalApiSlice } from '@/redux/features/api/internalApiSlice';
import themeSliceReducer from './features/theme/theme.slice';

const rootReducer = combineReducers({
    [externalApiSlice.reducerPath]: externalApiSlice.reducer,
    [internalApiSlice.reducerPath]: internalApiSlice.reducer,
    theme: themeSliceReducer
});

export default rootReducer;
