import {Button, Modal, Form} from 'react-bootstrap';
import React, {useEffect, useState} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';


import AuthComponent from '../AuthComponent';
import '../../styles/components/configuration-components/ImportConfigModal.scss';
import {faCheck, faCross} from '@fortawesome/free-solid-svg-icons';


type Props = {
  show: boolean,
  onClick: () => void
}


const UploadStatuses = {
  clean: 'clean',
  success: 'success',
  error: 'error'
}


const UploadStatusIcon = (props: { status: string }) => {
  switch (props.status) {
    case UploadStatuses.success:
      return (<FontAwesomeIcon icon={faCheck} className={'success'}/>);
    case UploadStatuses.error:
      return (<FontAwesomeIcon icon={faCross} className={'error'}/>);
    default:
      return null;
  }
}

// TODO add types
const ConfigImportModal = (props: Props) => {
  // TODO implement the back end
  const configImportEndpoint = '/api/temp_configuration';

  const [uploadStatus, setUploadStatus] = useState(UploadStatuses.clean);
  const [importDisabled, setImportDisabled] = useState(true);
  const [configContents, setConfigContents] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const authComponent = new AuthComponent({});

  useEffect(() => {
    if (configContents !== '') {
      sendConfigToServer();
    }
  }, [configContents])


  function sendConfigToServer() {
    authComponent.authFetch(configImportEndpoint,
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
        if (res.status == 200) {
          setImportDisabled(false);
        }
      })
  }


  function uploadFile(event) {
    let reader = new FileReader();
    reader.onload = (event) => {
      setConfigContents(JSON.stringify(event.target.result))
    };
    reader.readAsText(event.target.files[0]);
    event.target.value = null;
  }

  function onImportClick() {
  }

  return (
    <Modal show={props.show}
           onHide={props.onClick}
           size={'lg'}
           className={'config-export-modal'}>
      <Modal.Header closeButton>
        <Modal.Title>Configuration import</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div key={'config-export-option'}
             className={`mb-3 export-type-radio-buttons`}>
          <Form>
            <Form.File id='exampleFormControlFile1'
                       label='Please choose a configuration file'
                       accept='.conf'
                       onChange={uploadFile}/>
            <UploadStatusIcon status={uploadStatus}/>
            {showPassword && <PasswordInput onChange={setPassword} />}
          </Form>

        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant={'info'}
                onClick={onImportClick}
                disabled={importDisabled}>
          Import
        </Button>
      </Modal.Footer>
    </Modal>)
}

const PasswordInput = (props: {
  onChange: (passValue) => void,
}) => {
  return (
    <div className={'config-export-password-input'}>
      <p>Encrypt with a password:</p>
      <Form.Control type='password'
                    placeholder='Password'
                    onChange={evt => (props.onChange(evt.target.value))}/>
    </div>
  )
}


export default ConfigImportModal;
