import React from 'react';
import { Severity } from '@/_components/lib/severity';
import { Variant } from '@/_components/lib/variant';
import MUIAlert from '@mui/material/Alert';
import { AlertProps as MUIAlertProps } from '@mui/material/Alert';

export interface AlertProps extends MUIAlertProps {
    children: React.ReactNode;
    severity?: Severity;
    variant?: Variant;
    icon?: React.ReactNode;
    title?: string;
}

const Alert = (props: AlertProps) => {
    const {
        children,
        variant = Variant.STANDARD,
        severity = Severity.INFO,
        ...rest
    } = props;
    return (
        <MUIAlert variant={variant} severity={severity} {...rest}>
            {children}
        </MUIAlert>
    );
};

export default Alert;
