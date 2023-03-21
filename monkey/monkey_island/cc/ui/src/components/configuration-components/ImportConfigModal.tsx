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
import {decryptText} from '../utils/PasswordBasedEncryptor';
import {
  reformatConfig,
  formatCredentialsForIsland
} from '../configuration-components/ReformatHook';

type Props = {
  show: boolean,
  schema: object,
  onClose: (importSuccessful: boolean) => void
}


const ConfigImportModal = (props: Props) => {
  const configImportEndpoint = '/api/agent-configuration';
  const credentialsEndpoint = '/api/propagation-credentials/configured-credentials';

  const [uploadStatus, setUploadStatus] = useState(UploadStatuses.clean);
  const [configContents, setConfigContents] = useState(null);
  const [configCredentials, setConfigCredentials] = useState(null);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [configEncrypted, setConfigEncrypted] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [unsafeOptionsVerified, setUnsafeOptionsVerified] = useState(false);
  const [showUnsafeOptionsConfirmation,
    setShowUnsafeOptionsConfirmation] = useState(false);
  const [fileFieldKey, setFileFieldKey] = useState(Date.now());

  const authComponent = new AuthComponent({});

  useEffect(() => {
    if (configContents !== null && configCredentials !== null) {
      tryImport();
    }
  }, [configContents, configCredentials, unsafeOptionsVerified])

  function tryImport() {
    if (configEncrypted && !showPassword) {
      setShowPassword(true);
    } else if (configEncrypted && showPassword) {
      decryptAndSetConfig();
    } else if (!unsafeOptionsVerified) {
      checkUnsafeOptions();
    } else {
      submitImport();
    }
  }

  function checkUnsafeOptions() {
    let unsafeSelected = true;
    try {
      unsafeSelected = isUnsafeOptionSelected(props.schema, configContents);
    } catch {
      setUploadStatus(UploadStatuses.error);
      setErrorMessage('Configuration file is corrupt or in an outdated format');
      return;
    }

    if (unsafeSelected) {
      setShowUnsafeOptionsConfirmation(true);
    } else {
      setUnsafeOptionsVerified(true);
    }
  }

  function decryptAndSetConfig() {
    try {
      let decryptedConfig = JSON.parse(decryptText(configContents, password));
      let decryptedConfigCredentials = JSON.parse(decryptText(configCredentials, password));
      setConfigEncrypted(false);
      setConfigContents(decryptedConfig);
      setConfigCredentials(decryptedConfigCredentials);
    } catch {
      setUploadStatus(UploadStatuses.error);
      setErrorMessage('Decryption failed: Password is wrong or the file is corrupted');
    }
  }

  function submitImport() {
    try {
      sendConfigToServer();
      sendConfigCredentialsToServer();
      setUploadStatus(UploadStatuses.success);
    } catch {
      setUploadStatus(UploadStatuses.error);
      setErrorMessage('Configuration file is corrupt or in an outdated format');
    }
  }

  function sendConfigCredentialsToServer() {
    let credentials = formatCredentialsForIsland(configCredentials);
    authComponent.authFetch(credentialsEndpoint,
      {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(credentials)
      }
    ).then(res => {
      if (res.ok) {
        resetState();
        props.onClose(true);
      } else {
        setUploadStatus(UploadStatuses.error);
        setErrorMessage('Configuration file is corrupt or in an outdated format.');
      }
    })
  }

  function sendConfigToServer() {
    authComponent.authFetch(configImportEndpoint,
      {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(configContents)
      }
    ).then(res => {
      if (res.ok) {
        resetState();
        props.onClose(true);
      } else {
        setUploadStatus(UploadStatuses.error);
        setErrorMessage('Configuration file is corrupt or in an outdated format');
      }
    })
  }

  function isImportDisabled(): boolean {
    // Don't allow import if password input is empty or there's an error
    return (showPassword && password === '') || (errorMessage !== '');
  }

  function resetState() {
    setUploadStatus(UploadStatuses.clean);
    setPassword('');
    setConfigContents(null);
    setConfigCredentials(null);
    setErrorMessage('');
    setShowPassword(false);
    setShowUnsafeOptionsConfirmation(false);
    setUnsafeOptionsVerified(false);
    setFileFieldKey(Date.now());  // Resets the file input
    setConfigEncrypted(false);
  }

  function uploadFile(event) {
    setShowPassword(false);
    let reader = new FileReader();
    reader.onload = (event) => {
      let importContents = null;
      try {
        let contents = event.target.result as string;
        importContents = JSON.parse(contents);
      } catch (e) {
        setErrorMessage('File is not in a valid json format');
        return
      }

      try {
        setConfigEncrypted(importContents['metadata']['encrypted']);
        setConfigContents(importContents['configuration']);
        setConfigCredentials(importContents['credentials']);
      } catch (e) {
        if (e instanceof TypeError) {
          setErrorMessage('Missing required fields; configuration file is most '
            + 'likely from an older version of Infection Monkey.')
        } else {
          throw e;
        }
      }
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
        <div className={`mb-3 config-import-option`}>
          {showVerificationDialog()}
          <Form>
            <Form.File id="importConfigFileSelector"
                       label="Please choose a configuration file"
                       accept=".conf"
                       onChange={uploadFile}
                       className={'file-input'}
                       key={fileFieldKey}/>
            <UploadStatusIcon status={uploadStatus}/>

            {showPassword && <PasswordInput onChange={(password) => {
              setPassword(password);
              setErrorMessage('')
            }}/>}

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
                onClick={tryImport}
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
      <Form.Control type="password"
                    placeholder="Password"
                    onChange={evt => (props.onChange(evt.target.value))}/>
    </div>
  )
}


export default ConfigImportModal;
