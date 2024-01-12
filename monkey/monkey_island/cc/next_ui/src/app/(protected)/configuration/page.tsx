'use client';
import React, { useState } from 'react';
import _ from 'lodash';
import CircularProgress from '@mui/material/CircularProgress';
import Stack from '@mui/material/Stack';
import CheckIcon from '@mui/icons-material/Check';
import ErrorIcon from '@mui/icons-material/Error';
import ConfigurationForm from '@/_components/configuration/configuration-form/ConfigurationForm';
import { formValidationFormats } from './ValidationFormats';
import { customizeValidator } from '@rjsf/validator-ajv8';
import { nanoid } from 'nanoid';
import {
    useGetAgentConfigurationQuery,
    usePostResetAgentConfigurationMutation,
    useGetAgentConfigurationSchemaQuery
} from '@/redux/features/api/islandApiSlice';
const configSaveAction = 'config-saved';

export default function ConfigurePage(props: { onStatusChange: () => void }) {
    const [credentialsErrors] = useState([]);
    const [lastAction] = useState('none');
    const [showConfigImportModal, setShowConfigImportModal] = useState(false);
    const validator = customizeValidator({
        customFormats: formValidationFormats
    });
    const { data: agentConfiguration } = useGetAgentConfigurationQuery();
    const { data: schema, isLoading: schemaIsLoading } =
        useGetAgentConfigurationSchemaQuery();
    const [resetAgentConfiguration] = usePostResetAgentConfigurationMutation();

    const onSubmit = () => {};

    const resetConfig = () => {
        resetAgentConfiguration();
    };

    const exportConfig = async () => {};

    const isSubmitDisabled = () => {
        if (_.isEmpty(agentConfiguration)) {
            return true;
        }
        return false;
    };

    const getContent = () => {
        return (
            <ConfigurationForm
                schema={schema}
                configuration={agentConfiguration}
                validator={validator}
            />
        );
    };

    return schemaIsLoading ? (
        <Stack className={'main'}>
            <CircularProgress />
        </Stack>
    ) : (
        <Stack className={'main'}>
            <h1 className="page-title">Monkey Configuration</h1>
            {getContent()}
            <div className="text-center">
                <button
                    type="submit"
                    onClick={onSubmit}
                    className="btn btn-success btn-lg"
                    style={{ margin: '5px' }}
                    disabled={isSubmitDisabled()}>
                    Submit
                </button>
                <button
                    type="button"
                    onClick={resetConfig}
                    className="btn btn-danger btn-lg"
                    style={{ margin: '5px' }}>
                    Reset to defaults
                </button>
            </div>
            <div className="text-center">
                <button
                    onClick={() => {
                        setShowConfigImportModal(true);
                    }}
                    className="btn btn-info btn-lg"
                    style={{ margin: '5px' }}>
                    Import config
                </button>
                <button
                    type="button"
                    onClick={exportConfig}
                    className="btn btn-info btn-lg"
                    style={{ margin: '5px' }}>
                    Export config
                </button>
            </div>
            <div>
                {lastAction === 'reset' ? (
                    <div className="alert alert-success">
                        <CheckIcon style={{ marginRight: '5px' }} />
                        Configuration reset successfully.
                    </div>
                ) : (
                    ''
                )}
                {lastAction === configSaveAction ? (
                    <div className="alert alert-success">
                        <CheckIcon style={{ marginRight: '5px' }} />
                        Configuration saved successfully.
                    </div>
                ) : (
                    ''
                )}
                {lastAction === 'invalid_credentials_configuration' ? (
                    <div className="alert alert-danger">
                        <ErrorIcon style={{ marginRight: '5px' }} />
                        An invalid configuration file was imported or submitted.
                        One or more of the credentials are invalid.
                        {credentialsErrors.length !== 0 ? (
                            <ul>
                                {credentialsErrors.map((error) => (
                                    <li key={nanoid()}>{error}</li>
                                ))}
                            </ul>
                        ) : (
                            ''
                        )}
                    </div>
                ) : (
                    ''
                )}
                {lastAction === 'invalid_configuration' ? (
                    <div className="alert alert-danger">
                        <ErrorIcon style={{ marginRight: '5px' }} />
                        An invalid configuration file was imported or submitted.
                    </div>
                ) : (
                    ''
                )}
                {lastAction === 'import_success' ? (
                    <div className="alert alert-success">
                        <CheckIcon style={{ marginRight: '5px' }} />
                        Configuration imported successfully.
                    </div>
                ) : (
                    ''
                )}
            </div>
        </Stack>
    );
}
