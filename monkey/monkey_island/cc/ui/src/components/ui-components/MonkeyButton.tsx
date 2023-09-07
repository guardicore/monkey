import React from 'react';
import Button from '@mui/material/Button';
import ComponentColor from './base-components/colors';
import {ThemeProvider} from '@mui/material';
import MUITheme from '../../styles/MUITheme';

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
    <ThemeProvider theme={MUITheme} >
      <Button {...styleProps} onClick={onClick} >
        {children}
      </Button>
    </ThemeProvider>
  )
}

export default MonkeyButton;
