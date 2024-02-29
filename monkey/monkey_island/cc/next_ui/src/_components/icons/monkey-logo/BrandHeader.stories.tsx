import type { Meta, StoryObj } from '@storybook/react';
import BrandHeader from './BrandHeader';

const meta = {
    title: 'icons/BrandHeader',
    component: BrandHeader,
    parameters: {
        layout: 'centered'
    },
    tags: ['autodocs'],
    argTypes: {
        color: { control: 'color' }
    }
} satisfies Meta<typeof BrandHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Colored: Story = {
    args: {
        color: 'red',
        sx: { height: '50px' }
    }
};
