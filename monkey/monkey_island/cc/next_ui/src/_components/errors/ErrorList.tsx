import React from 'react';
import Alert from '@/_components/alerts/Alert';
import { Severity } from '@/_components/lib/severity';

export interface ErrorAlertsProps {
    errors: string[];
}

const ErrorList = (props: ErrorAlertsProps) => {
    const { errors } = props;

    return errors.map((error, index) => (
        <Alert key={index} severity={Severity.ERROR} sx={{ mb: '10px' }}>
            {error}
        </Alert>
    ));
};

export default ErrorList;
