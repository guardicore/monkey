import type { Meta, StoryObj } from '@storybook/react';
import LoginPage from './page';
import { RootProvider } from '@/providers/RootProvider';
import { rest } from 'msw';

const meta = {
    title: 'pages/LoginPage',
    component: LoginPage,
    parameters: {
        layout: 'centered'
    },
    tags: ['autodocs']
} satisfies Meta<typeof LoginPage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = {
    decorators: [(story) => <RootProvider>{story()}</RootProvider>],
    parameters: {
        msw: {
            handlers: [
                rest.post('api/login', (req, res, ctx) => {
                    return res(
                        ctx.json({
                            response: {
                                user: {
                                    authentication_token: 'token',
                                    token_ttl_sec: 1000
                                }
                            }
                        })
                    );
                })
            ]
        }
    }
};

export const Error: Story = {
    decorators: [(story) => <RootProvider>{story()}</RootProvider>],
    parameters: {
        msw: {
            handlers: [
                rest.post('api/login', (req, res, ctx) => {
                    return res(
                        ctx.json({
                            data: {
                                response: {
                                    errors: ['Incorrect password']
                                }
                            }
                        })
                    );
                })
            ]
        }
    }
};
