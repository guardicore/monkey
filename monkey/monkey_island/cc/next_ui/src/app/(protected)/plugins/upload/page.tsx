'use client';
import React, { useCallback, useMemo, useState } from 'react';
import Alert from '@mui/material/Alert';
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

const UploadNewPlugin = () => {
    const [plugin, setPlugin] = useState(null);
    const [loading] = useState(false);
    const [showSuccessAlert, setShowSuccessAlert] = useState(false);
    const [pluginName, setPluginName] = useState('');
    const [errors, setErrors] = useState([]);

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

    const onDrop = useCallback((acceptedPlugin, rejectedPlugin) => {
        if (acceptedPlugin?.length) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (e.target.readyState === FileReader.DONE) {
                    const binaryPlugin = new Uint8Array(e.target.result);
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

    const uploadPlugin = () => {};

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
                {plugin === null && !loading && (
                    <div>
                        <Typography>
                            Drag &apos;n&apos; drop Plugin Tar here
                        </Typography>
                        <Typography textAlign="center">
                            or click to select a file
                        </Typography>
                    </div>
                )}
                {plugin !== null && !loading && (
                    <Typography>
                        &apos;{pluginName}&apos; is ready to be uploaded.
                    </Typography>
                )}
                {loading && (
                    <div>
                        <Typography>
                            Uploading &apos;{pluginName}&apos; to Island!
                        </Typography>
                        <MonkeyLoadingIcon />
                    </div>
                )}
            </MonkeyFileUpload>

            {showSuccessAlert && (
                <Alert
                    severity="success"
                    onClose={() => setShowSuccessAlert(false)}>
                    <AlertTitle>
                        &apos;{pluginName}&apos; is successfully installed
                    </AlertTitle>
                </Alert>
            )}
            {showErrors && (
                <Alert severity="error" onClose={() => setErrors([])}>
                    <AlertTitle>Error uploading Plugin Tar</AlertTitle>
                    <ul id="circle-list">
                        {errors.map((error, index) => (
                            <Typography key={index} component="li">
                                {error}
                            </Typography>
                        ))}
                    </ul>
                </Alert>
            )}
            <br />
            <Grid
                container
                direction="row"
                justifyContent="center"
                alignItems="center"
                spacing={1}>
                <Grid item>
                    <Button
                        variant="contained"
                        disabled={plugin === null || loading}
                        startIcon={<FileUploadIcon />}
                        onClick={() => uploadPlugin()}>
                        Upload Plugin
                    </Button>
                </Grid>
                <Grid item>
                    {plugin !== null && (
                        <Button
                            variant="outlined"
                            color="error"
                            disabled={loading}
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
