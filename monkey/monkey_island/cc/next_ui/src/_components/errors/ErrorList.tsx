import React from 'react';
import MonkeyAlert from '@/_components/alerts/MonkeyAlert';
import { Severity } from '@/_components/lib/severity';

export interface ErrorAlertsProps {
    errors: string[];
}

const ErrorList = (props: ErrorAlertsProps) => {
    const { errors } = props;

    return errors.map((error, index) => (
        <MonkeyAlert key={index} severity={Severity.ERROR} sx={{ mb: '10px' }}>
            {error}
        </MonkeyAlert>
    ));
};

export default ErrorList;
