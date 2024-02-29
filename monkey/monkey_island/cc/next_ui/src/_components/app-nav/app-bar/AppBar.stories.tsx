import type { Meta, StoryObj } from '@storybook/react';
import AppBar from './AppBar';
import { Provider } from 'react-redux';
import { configureStore, createSlice } from '@reduxjs/toolkit';

const Mockstore = ({ children }) => (
    <Provider
        store={configureStore({
            reducer: {
                logout: createSlice({
                    name: 'logout',
                    initialState: {},
                    reducers: {
                        // eslint-disable-next-line @typescript-eslint/no-unused-vars
                        logout: (_state, _action) => {}
                    }
                }).reducer
            }
        })}>
        {children}
    </Provider>
);

const meta = {
    title: 'app-nav/AppBar',
    component: AppBar,
    parameters: {
        layout: 'centered'
    },
    tags: ['autodocs']
} satisfies Meta<typeof AppBar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
    decorators: [(story) => <Mockstore>{story()}</Mockstore>]
};
