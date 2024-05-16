'use client';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import AlertTitle from '@mui/material/AlertTitle';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import Box from '@mui/material/Box';
import MonkeyFileUpload, {
    UploadStatus
} from '@/_components/file-upload/MonkeyFileUpload';
import { useUploadPluginMutation } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import MonkeyAlert from '@/_components/alerts/MonkeyAlert';
import { Severity } from '@/_components/lib/severity';

const UploadNewPlugin = () => {
    const [upload, { isError, error, isLoading, isSuccess }] =
        useUploadPluginMutation();
    const [plugin, setPlugin] = useState<null | Uint8Array>(null);
    const [showSuccessAlert, setShowSuccessAlert] = useState(false);
    const [pluginName, setPluginName] = useState('');
    const [errors, setErrors] = useState<any[]>([]);

    const uploadStatus = useMemo(() => {
        if (plugin !== null) {
            return UploadStatus.ACCEPTED;
        } else if (errors.length !== 0) {
            return UploadStatus.REJECTED;
        } else {
            return UploadStatus.IDLE;
        }
    }, [plugin, errors]);

    const showErrors = useMemo(() => {
        return errors.length !== 0;
    }, [errors]);

    useEffect(() => {
        if (isSuccess) {
            setShowSuccessAlert(true);
            setPlugin(null);
        }
    }, [isSuccess]);

    useEffect(() => {
        if (isError) {
            setErrors([error.data]);
            setPlugin(null);
        }
    }, [error]);

    const onDrop = useCallback((acceptedPlugin, rejectedPlugin) => {
        setErrors([]);
        setShowSuccessAlert(false);
        if (acceptedPlugin?.length) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (e.target?.readyState === FileReader.DONE) {
                    const binaryPlugin = new Uint8Array(
                        e.target.result as ArrayBuffer
                    );
                    setPlugin(binaryPlugin);
                    setPluginName(Object.assign(acceptedPlugin?.[0]).name);
                }
            };
            reader.readAsArrayBuffer(acceptedPlugin?.[0]);
        }
        if (rejectedPlugin?.length) {
            const uniqueErrors = new Set();

            rejectedPlugin.forEach((item) => {
                item.errors.forEach((error) => {
                    uniqueErrors.add(`${error.message}`);
                });
            });
            setErrors(Array.from(uniqueErrors));
        }
    }, []);

    const uploadPlugin = () => {
        if (plugin === null) {
            return;
        }
        upload(plugin);
    };

    const removePlugin = () => {
        setPlugin(null);
        setPluginName('');
        setErrors([]);
    };

    return (
        <Box sx={{ mt: '20px' }}>
            <MonkeyFileUpload
                onDrop={onDrop}
                maxFiles={1}
                accept={{ 'application/x-tar': [] }}
                uploadStatus={uploadStatus}>
                {plugin === null && !isLoading && (
                    <div>
                        <Typography>
                            Drag &apos;n&apos; drop Plugin Tar here
                        </Typography>
                        <Typography textAlign="center">
                            or click to select a file
                        </Typography>
                    </div>
                )}
                {plugin !== null && !isLoading && (
                    <Typography>
                        &apos;{pluginName}&apos; is ready to be uploaded.
                    </Typography>
                )}
                {isLoading && (
                    <div>
                        <Typography>
                            Uploading &apos;{pluginName}&apos; to Island!
                        </Typography>
                    </div>
                )}
            </MonkeyFileUpload>

            <Box sx={{ mt: '10px', mb: '10px' }}>
                {showSuccessAlert && (
                    <MonkeyAlert
                        severity={Severity.SUCCESS}
                        onClose={() => setShowSuccessAlert(false)}>
                        <AlertTitle>
                            &apos;{pluginName}&apos; was successfully installed!
                        </AlertTitle>
                    </MonkeyAlert>
                )}
                {showErrors && (
                    <MonkeyAlert
                        severity={Severity.ERROR}
                        onClose={() => setErrors([])}>
                        <AlertTitle>Error uploading Plugin Tar</AlertTitle>
                        <ul id="circle-list">
                            {errors.map((error, index) => (
                                <Typography key={index} component="li">
                                    {error}
                                </Typography>
                            ))}
                        </ul>
                    </MonkeyAlert>
                )}
            </Box>

            <Grid
                container
                direction="row"
                justifyContent="center"
                alignItems="center"
                spacing={1}>
                <Grid item>
                    <Button
                        variant="contained"
                        disabled={plugin === null || isLoading}
                        startIcon={
                            isLoading ? (
                                <MonkeyLoadingIcon />
                            ) : (
                                <FileUploadIcon />
                            )
                        }
                        onClick={() => uploadPlugin()}>
                        Upload Plugin
                    </Button>
                </Grid>
                <Grid item>
                    {plugin !== null && (
                        <Button
                            variant="outlined"
                            color="error"
                            disabled={isLoading}
                            startIcon={<DeleteIcon />}
                            onClick={() => removePlugin()}>
                            Cancel
                        </Button>
                    )}
                </Grid>
            </Grid>
        </Box>
    );
};

export default UploadNewPlugin;
