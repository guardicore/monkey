'use client';

import { createSlice } from '@reduxjs/toolkit';
import { clearTimeout } from 'timers';

interface AuthenticationTimerState {
    timer: NodeJS.Timeout | null;
}

interface TimerActionType {
    payload: NodeJS.Timeout;
    type: string;
}

const initialState = { timer: null } as AuthenticationTimerState;

const authenticationTimerSlice = createSlice({
    name: 'authenticationTimeout',
    initialState,
    reducers: {
        clearTimer(state: AuthenticationTimerState) {
            if (state.timer) {
                clearTimeout(state.timer);
            }
        },
        setTimer(state: AuthenticationTimerState, action: TimerActionType) {
            state.timer = action.payload;
        }
    }
});

export const { setTimer, clearTimer } = authenticationTimerSlice.actions;
export default authenticationTimerSlice.reducer;
