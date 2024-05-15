import React from 'react';
import { useTheme } from '@mui/material/styles';
import MUIAlert, { AlertProps as MUIAlertProps } from '@mui/material/Alert';
import { Severity } from '@/_components/lib/severity';
import { Variant } from '@/_components/lib/variant';

export interface AlertProps extends MUIAlertProps {
    children: React.ReactNode;
    severity?: Severity;
    variant?: Variant;
    icon?: React.ReactNode;
    title?: string;
}

const MonkeyAlert = (props: AlertProps) => {
    const theme = useTheme();
    const {
        children,
        variant = theme.palette.mode === 'light'
            ? Variant.STANDARD
            : Variant.OUTLINED,
        severity = Severity.INFO,
        ...rest
    } = props;
    return (
        <MUIAlert variant={variant} severity={severity} {...rest}>
            {children}
        </MUIAlert>
    );
};

export default MonkeyAlert;
