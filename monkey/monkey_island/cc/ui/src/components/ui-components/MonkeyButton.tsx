import React from 'react';
import Button from '@mui/material/Button';
import ComponentColor from './base-components/colors';

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
  color?: ComponentColor;
  disabled?: boolean;
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const MonkeyButton = (props: MonkeyButtonProps) => {
  let {children, onClick, ...styleProps} = props;
  return (
    <Button {...styleProps} onClick={onClick}>
      {children}
    </Button>
  )
}

export default MonkeyButton;
