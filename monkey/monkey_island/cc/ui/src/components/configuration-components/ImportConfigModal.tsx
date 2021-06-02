import {Button, Modal, Form, Alert} from 'react-bootstrap';
import React, {useEffect, useState} from 'react';

import AuthComponent from '../AuthComponent';
import '../../styles/components/configuration-components/ImportConfigModal.scss';
import UploadStatusIcon, {UploadStatuses} from '../ui-components/UploadStatusIcon';
import {faExclamationCircle} from '@fortawesome/free-solid-svg-icons/faExclamationCircle';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';


type Props = {
  show: boolean,
  onClose: (importSuccessful: boolean) => void
}


const ConfigImportModal = (props: Props) => {
  const configImportEndpoint = '/api/configuration/import';

  const [uploadStatus, setUploadStatus] = useState(UploadStatuses.clean);
  const [configContents, setConfigContents] = useState(null);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const authComponent = new AuthComponent({});

  useEffect(() => {
    if (configContents !== null) {
      sendConfigToServer();
    }
  }, [configContents])


  function sendConfigToServer(): Promise<string> {
    return authComponent.authFetch(configImportEndpoint,
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          config: configContents,
          password: password
        })
      }
    ).then(res => res.json())
      .then(res => {
        if (res['import_status'] === 'password_required') {
          setShowPassword(true);
        } else if (res['import_status'] === 'wrong_password'){
          setErrorMessage(res['message']);
        }
        if (res['import_status'] === 'invalid_configuration'){
          setUploadStatus(UploadStatuses.error);
          setErrorMessage(res['message']);
        } else {
          setUploadStatus(UploadStatuses.success);
        }
        return res['import_status'];
      })
  }

  function isImportDisabled(): boolean {
    return uploadStatus !== UploadStatuses.success
  }

  function resetState() {
    setUploadStatus(UploadStatuses.clean);
    setPassword('');
    setConfigContents(null);
    setErrorMessage('');
    setShowPassword(false);
  }

  function uploadFile(event) {
    let reader = new FileReader();
    reader.onload = (event) => {
      setConfigContents(event.target.result);
    };
    reader.readAsText(event.target.files[0]);

  }

  function onImportClick() {
    sendConfigToServer().then((importStatus) => {
      if(importStatus === 'imported'){
        resetState();
        props.onClose(true);
      }
    });
  }

  return (
    <Modal show={props.show}
           onHide={()=> {resetState(); props.onClose(false)}}
           size={'lg'}
           className={'config-import-modal'}>
      <Modal.Header closeButton>
        <Modal.Title>Configuration import</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className={`mb-3 config-import-option`}>
          <Form>
            <Form.File id='exampleFormControlFile1'
                       label='Please choose a configuration file'
                       accept='.conf'
                       onChange={uploadFile}
                        className={'file-input'}/>
            <UploadStatusIcon status={uploadStatus}/>

            {showPassword && <PasswordInput onChange={setPassword} />}

            { errorMessage &&
              <Alert variant={'danger'} className={'import-error'}>
                <FontAwesomeIcon icon={faExclamationCircle} style={{'marginRight': '5px'}}/>
                {errorMessage}
              </Alert>
            }
          </Form>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant={'info'}
                onClick={onImportClick}
                disabled={isImportDisabled()}>
          Import
        </Button>
      </Modal.Footer>
    </Modal>)
}

const PasswordInput = (props: {
  onChange: (passValue) => void,
}) => {
  return (
    <div className={'config-import-password-input'}>
      <p>File is protected. Please enter the password:</p>
      <Form.Control type='password'
                    placeholder='Password'
                    onChange={evt => (props.onChange(evt.target.value))}/>
    </div>
  )
}


export default ConfigImportModal;
