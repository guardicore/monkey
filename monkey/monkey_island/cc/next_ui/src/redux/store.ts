import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './rootReducer';
import { CurriedGetDefaultMiddleware } from '@reduxjs/toolkit/src/getDefaultMiddleware';
import { externalApiSlice } from '@/redux/features/api/externalApiSlice';
import { internalApiSlice } from '@/redux/features/api/internalApiSlice';

const REDUX_LOGGER_ENABLED =
    process.env.NEXT_PUBLIC_REDUX_LOGGER_ENABLED ===
    process.env.NEXT_PUBLIC_TRUE_VALUE;

const getMiddlewares = (getDefaultMiddleware: CurriedGetDefaultMiddleware) => {
    const middlewares: any[] = [
        externalApiSlice.middleware,
        internalApiSlice.middleware
    ];

    if (REDUX_LOGGER_ENABLED) {
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        const { logger } = require('redux-logger');

        const devMiddlewares = [...middlewares, ...[logger]];
        return getDefaultMiddleware().concat(devMiddlewares);
    }

    // @ts-ignore
    return getDefaultMiddleware().concat(middlewares);
};

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => getMiddlewares(getDefaultMiddleware),
    devTools: process.env.NODE_ENV !== process.env.NEXT_PUBLIC_PRODUCTION_KEY
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
