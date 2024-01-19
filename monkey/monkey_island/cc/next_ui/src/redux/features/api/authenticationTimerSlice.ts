'use client';

import { createSlice } from '@reduxjs/toolkit';
import { clearTimeout } from 'timers';

interface AuthenticationTimerState {
    timer: NodeJS.Timeout | null;
}

const initialState = { timer: null } as AuthenticationTimerState;

const authenticationTimerSlice = createSlice({
    name: 'authenticationTimeout',
    initialState,
    reducers: {
        setTimer(state, timer) {
            if (state.timer) {
                this.clearTimer(state);
            }
            state.timer = timer;
        },
        clearTimer(state: AuthenticationTimerState) {
            if (state.timer) {
                clearTimeout(state.timer);
            }
        }
    }
});

export const { setTimer, clearTimer } = authenticationTimerSlice.actions;
export default authenticationTimerSlice.reducer;
