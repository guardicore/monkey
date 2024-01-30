import React from 'react';
import Alert from '@/_components/alerts/Alert';
import { Severity } from '@/_components/lib/severity';
import classes from './errorAlerts.module.scss';

export interface ErrorAlertsProps {
    errors: string[];
}

const ErrorAlerts = (props: ErrorAlertsProps) => {
    const { errors } = props;

    return errors.map((error, index) => (
        <Alert
            key={index}
            severity={Severity.ERROR}
            id={classes['error-alerts']}>
            {error}
        </Alert>
    ));
};

export default ErrorAlerts;
