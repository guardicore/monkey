import type { Meta, StoryObj } from '@storybook/react';
import AppMenu from './AppMenu';

const meta = {
    title: 'app-nav/AppMenu',
    component: AppMenu,
    parameters: {
        layout: 'centered'
    },
    tags: ['autodocs'],
    argTypes: {
        orientation: { control: 'text', options: ['vertical', 'horizontal'] }
    }
} satisfies Meta<typeof AppMenu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Horizontal: Story = {
    args: {
        orientation: 'horizontal'
    }
};

export const Vertical: Story = {
    args: {
        orientation: 'vertical'
    }
};
