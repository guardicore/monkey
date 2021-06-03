import {Button, Modal, Form, Alert} from 'react-bootstrap';
import React, {useEffect, useState} from 'react';
import {faExclamationCircle} from '@fortawesome/free-solid-svg-icons/faExclamationCircle';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

import AuthComponent from '../AuthComponent';
import '../../styles/components/configuration-components/ImportConfigModal.scss';
import UnsafeConfigOptionsConfirmationModal
  from './UnsafeConfigOptionsConfirmationModal.js';
import UploadStatusIcon, {UploadStatuses} from '../ui-components/UploadStatusIcon';
import isUnsafeOptionSelected from '../utils/SafeOptionValidator.js';


type Props = {
  show: boolean,
  onClose: (importSuccessful: boolean) => void
}


const ConfigImportModal = (props: Props) => {
  const configImportEndpoint = '/api/configuration/import';

  const [uploadStatus, setUploadStatus] = useState(UploadStatuses.clean);
  const [configContents, setConfigContents] = useState(null);
  const [candidateConfig, setCandidateConfig] = useState(null);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [unsafeOptionsVerified, setUnsafeOptionsVerified] = useState(false);
  const [showUnsafeOptionsConfirmation,
    setShowUnsafeOptionsConfirmation] = useState(false);
  const [fileFieldKey, setFileFieldKey] = useState(Date.now());

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
          password: password,
          unsafeOptionsVerified: unsafeOptionsVerified
        })
      }
    ).then(res => res.json())
      .then(res => {
        if (res['import_status'] === 'password_required') {
          setUploadStatus(UploadStatuses.success);
          setShowPassword(true);
        } else if (res['import_status'] === 'wrong_password') {
          setErrorMessage(res['message']);
        } else if (res['import_status'] === 'invalid_configuration') {
          setUploadStatus(UploadStatuses.error);
          setErrorMessage(res['message']);
        } else if (res['import_status'] === 'unsafe_options_verification_required') {
          if (isUnsafeOptionSelected(res['config_schema'], res['config'])) {
            setShowUnsafeOptionsConfirmation(true);
            setCandidateConfig(JSON.stringify(res['config']));
          } else {
            setUnsafeOptionsVerified(true);
            setConfigContents(res['config']);
          }
        } else if (res['import_status'] === 'imported'){
          resetState();
          props.onClose(true);
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
    setShowUnsafeOptionsConfirmation(false);
    setUnsafeOptionsVerified(false);
    setFileFieldKey(Date.now());  // Resets the file input
  }

  function uploadFile(event) {
    let reader = new FileReader();
    reader.onload = (event) => {
      setConfigContents(event.target.result);
    };
    reader.readAsText(event.target.files[0]);
  }

  function showVerificationDialog() {
    return (
      <UnsafeConfigOptionsConfirmationModal
        show={showUnsafeOptionsConfirmation}
        onCancelClick={() => {
          resetState();
        }}
        onContinueClick={() => {
          setUnsafeOptionsVerified(true);
          setConfigContents(candidateConfig);
        }}
      />
    );
  }

  return (
    <
      Modal
      show={props.show}
      onHide={() => {
        resetState();
        props.onClose(false)
      }}
      size={'lg'}
      className={'config-import-modal'}>
      < Modal.Header
        closeButton>
        < Modal.Title>
          Configuration
          import
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {showVerificationDialog()}
        <div className={`mb-3 config-import-option`}>
          <Form>
            <Form.File id='importConfigFileSelector'
                       label='Please choose a configuration file'
                       accept='.conf'
                       onChange={uploadFile}
                       className={'file-input'}
                       key={fileFieldKey}/>
            <UploadStatusIcon status={uploadStatus}/>

            {showPassword && <PasswordInput onChange={setPassword}/>}

            {errorMessage &&
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
                onClick={sendConfigToServer}
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
