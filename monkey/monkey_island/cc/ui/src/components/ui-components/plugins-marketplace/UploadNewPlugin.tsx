import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import IslandHttpClient, { APIEndpoint } from '../../IslandHttpClient';
import LoadingIcon from '../LoadingIcon';
import '../../../styles/components/plugins-marketplace/UploadNewPlugin.scss';

const getColor = (props) => {
  if (props.isDragAccept) {
    return '#00e676';
  }
  if (props.isDragReject) {
    return '#ff1744';
  }
  if (props.isFocused) {
    return '#ffc107';
  }
  return '#eeeeee';
};

const UploadNewPlugin = () => {
  const [plugin, setPlugin] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  const [showErrorAlert, setShowErrorAlert] = useState(false);
  const [pluginName, setPluginName] = useState('');
  const [errors, setErrors] = useState([]);

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

      rejectedPlugin.forEach(item => {
        item.errors.forEach(error => {
          uniqueErrors.add(`${error.message}`);
        });
      });
      setErrors(Array.from(uniqueErrors));
      showErrorAlertDialog();
    }
  }, []);

  const {
    getRootProps,
    getInputProps,
    isDragAccept,
    isFocused,
    isDragReject
  } = useDropzone({
    accept: {
      'application/x-tar': []
    },
    maxFiles: 1,
    onDrop
  });

  const showErrorAlertDialog = () => {
    setShowErrorAlert(true);
    setTimeout(() => {
      setShowErrorAlert(false);
      setErrors([]);
    }, 10000);
  }

  const uploadPlugin = () => {
    setLoading(true);
    IslandHttpClient.put(APIEndpoint.installAgentPlugin, plugin, false).then(res => {
      setLoading(false);
      if (res.status === 200) {
        setShowSuccessAlert(true);
        setTimeout(() => {
          setShowSuccessAlert(false);
          setPluginName('');
        }, 10000);
        setPlugin(null);
      } else {
        let error = `Error occurred installing the plugin archive '${pluginName}'`;
        setErrors(prevErrs => [...prevErrs, error]);
        setPlugin(null);
        setPluginName('');
        showErrorAlertDialog();
      }
    });
  };

  const removePlugin = () => {
    setPlugin(null);
    setPluginName('');
    setErrors([]);
  };

  const containerStyle = {
    borderColor: getColor({ isDragAccept, isFocused, isDragReject })
  };

  return (
    <div className="container">
      <div
        className="drop-zone"
        style={containerStyle}
        {...getRootProps({ isDragAccept, isFocused, isDragReject })}
      >
        <input {...getInputProps()} />
        {plugin === null && !loading && (
          <div>
            <Typography>Drag 'n' drop Plugin Tar here</Typography>
            <Typography textAlign="center">or click to select a file</Typography>
          </div>
        )}
        {plugin !== null && !loading && (
          <Typography>'{pluginName}' is ready to be uploaded.</Typography>
        )}
        {loading && (
          <div>
            <Typography>Uploading '{pluginName}' to Island!</Typography>
            <LoadingIcon />
          </div>
        )}
      </div>
      {showSuccessAlert && (
        <Alert severity="success" onClose={() => setShowSuccessAlert(false)}>
          <AlertTitle>'{pluginName}' is successfully installed</AlertTitle>
        </Alert>
      )}
      {showErrorAlert && (
        <Alert severity="error" onClose={() => setShowErrorAlert(false)}>
          <AlertTitle>Error uploading Plugin Tar</AlertTitle>
          <ul className="circle-list">
            {errors.map((error, index) => (
              <Typography key={index} component="li">
                {error}
              </Typography>
            ))}
          </ul>
        </Alert>
      )}
      <br />
      <Grid container direction="row" justifyContent="center" alignItems="center" spacing={1}>
        <Grid item>
          <Button
            variant="contained"
            disabled={plugin === null || loading}
            startIcon={<FileUploadIcon />}
            onClick={() => uploadPlugin()}
          >
            Upload Plugin
          </Button>
        </Grid>
        <Grid item>
          {plugin !== null && (
            <Button
              variant="outlined"
              color="error"
              disabled={plugin === null || loading}
              startIcon={<DeleteIcon />}
              onClick={() => removePlugin()}
            >
              Cancel
            </Button>
          )}
        </Grid>
      </Grid>
    </div>
  );
};

export default UploadNewPlugin;
