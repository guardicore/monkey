import type { Meta, StoryObj } from '@storybook/react';
import LoadingIcon from './LoadingIcon';

const meta = {
    title: 'icons/LoadingIcon',
    component: LoadingIcon,
    parameters: {
        layout: 'centered'
    },
    tags: ['autodocs']
} satisfies Meta<typeof LoadingIcon>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
