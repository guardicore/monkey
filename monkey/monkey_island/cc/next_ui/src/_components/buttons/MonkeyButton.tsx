import React from 'react';
import Button from '@mui/material/Button';

export enum ButtonVariant {
    Contained = 'contained',
    Outlined = 'outlined',
    Text = 'text'
}

export enum ButtonSize {
    Small = 'small',
    Medium = 'medium',
    Large = 'large'
}

type MonkeyButtonProps = {
    onClick?: () => void;
    children: React.ReactNode;
    disabled?: boolean;
    variant?: ButtonVariant;
    size?: ButtonSize;
};

const MonkeyButton = (props: MonkeyButtonProps) => {
    const { children, onClick, ...rest } = props;
    return (
        <Button onClick={onClick} {...rest}>
            {children}
        </Button>
    );
};

export default MonkeyButton;
