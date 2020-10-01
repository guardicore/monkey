import React, {useEffect, useState} from 'react';
import InlineSelection from '../../../../ui-components/inline-selection/InlineSelection';
import {COLUMN_SIZES} from '../../../../ui-components/inline-selection/utils';
import AWSSetupOptions from './AWSSetupOptions';
import {Button, Col, Form, Row} from 'react-bootstrap';
import AuthComponent from '../../../../AuthComponent';
import '../../../../../styles/components/scoutsuite/AWSSetup.scss';
import {PROVIDERS} from '../ProvidersEnum';
import classNames from 'classnames';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faChevronDown} from '@fortawesome/free-solid-svg-icons/faChevronDown';
import {faChevronUp} from '@fortawesome/free-solid-svg-icons/faChevronUp';
import {faQuestion} from '@fortawesome/free-solid-svg-icons';
import Collapse from '@kunukn/react-collapse/dist/Collapse.umd';
import keySetupForAnyUserImage from '../../../../../images/aws_keys_tutorial-any-user.png';
import keySetupForCurrentUserImage from '../../../../../images/aws_keys_tutorial-current-user.png';
import ImageModal from '../../../../ui-components/ImageModal';


export default function AWSCLISetup(props) {
  return InlineSelection(getContents, {
    ...props,
    collumnSize: COLUMN_SIZES.LARGE,
    onBackButtonClick: () => {
      props.setComponent(AWSSetupOptions, props);
    }
  })
}

const authComponent = new AuthComponent({})

const getContents = (props) => {

  const [accessKeyId, setAccessKeyId] = useState('');
  const [secretAccessKey, setSecretAccessKey] = useState('');
  const [sessionToken, setSessionToken] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [docCollapseOpen, setDocCollapseOpen] = useState(false);

  function submitKeys(event) {
    event.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');
    authComponent.authFetch(
      '/api/scoutsuite_auth/' + PROVIDERS.AWS,
      {
        'method': 'POST',
        'body': JSON.stringify({
          'accessKeyId': accessKeyId,
          'secretAccessKey': secretAccessKey,
          'sessionToken': sessionToken
        })
      })
      .then(res => res.json())
      .then(res => {
        if (res['error_msg'] === '') {
          setSuccessMessage('AWS keys saved!');
        } else {
          setErrorMessage(res['error_msg']);
        }
      });
  }

  useEffect(() => {
    authComponent.authFetch('/api/aws_keys')
      .then(res => res.json())
      .then(res => {
        setAccessKeyId(res['access_key_id']);
        setSecretAccessKey(res['secret_access_key']);
        setSessionToken(res['session_token']);
      });
  }, [props]);


  // TODO separate into standalone component
  function getKeyCreationDocsContent() {
    return (
      <div className={'key-creation-tutorial'}>
        <h5>Tips</h5>
        <p>Consider creating a new user account just for this activity. Assign only <b>ReadOnlyAccess</b> and&nbsp;
        <b>SecurityAudit</b> policies.</p>

        <h5>Keys for custom user</h5>
        <p>1. Open the IAM console at <a href={'https://console.aws.amazon.com/iam/'}
                                         target={'_blank'}>https://console.aws.amazon.com/iam/</a> .</p>
        <p>2. In the navigation pane, choose Users.</p>
        <p>3. Choose the name of the user whose access keys you want to create, and then choose the Security credentials
          tab.</p>
        <p>4. In the Access keys section, choose Create access key.</p>
        <p>To view the new access key pair, choose Show. Your credentials will look something like this:</p>
        <p>Access key ID: AKIAIOSFODNN7EXAMPLE</p>
        <p>Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY</p>
        <Row>
          <Col lg={3} md={3} sm={5} xs={12}>
            <ImageModal image={keySetupForAnyUserImage}/>
          </Col>
        </Row>

        <h5>Keys for current user</h5>
        <p>1. Click on your username in the upper right corner.</p>
        <p>2. Click on "My security credentials".</p>
        <p>3. In the Access keys section, choose Create access key.</p>
        <p>To view the new access key pair, choose Show. Your credentials will look something like this:</p>
        <p>Access key ID: AKIAIOSFODNN7EXAMPLE</p>
        <p>Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY</p>
        <Row>
          <Col lg={3} md={3} sm={5} xs={12}>
            <ImageModal image={keySetupForCurrentUserImage}/>
          </Col>
        </Row>
      </div>);
  }

  function getKeyCreationDocs() {
    return (
      <div className={classNames('collapse-item', {'item--active': docCollapseOpen})}>
        <button className={'btn-collapse'}
                onClick={() => setDocCollapseOpen(!docCollapseOpen)}>
          <span>
            <FontAwesomeIcon icon={faQuestion} className={'question-icon'}/>
            <p>How to generate keys</p>
          </span>
          <span>
              <FontAwesomeIcon icon={docCollapseOpen ? faChevronDown : faChevronUp}/>
          </span>
        </button>
        <Collapse
          className='collapse-comp'
          isOpen={docCollapseOpen}
          render={getKeyCreationDocsContent}/>
      </div>);
  }

  return (
    <div className={'aws-scoutsuite-key-configuration'}>
      {getKeyCreationDocs()}
      <Form className={'auth-form'} onSubmit={submitKeys}>
        <Form.Control onChange={evt => setAccessKeyId(evt.target.value)}
                      type='text'
                      placeholder='Access key ID'
                      value={accessKeyId}/>
        <Form.Control onChange={evt => setSecretAccessKey(evt.target.value)}
                      type='password'
                      placeholder='Secret access key'
                      value={secretAccessKey}/>
        <Form.Control onChange={evt => setSessionToken(evt.target.value)}
                      type='text'
                      placeholder='Session token (optional, only for temp. keys)'
                      value={sessionToken}/>
        {
          errorMessage ?
            <div className="alert alert-danger" role="alert">{errorMessage}</div>
            :
            ''
        }
        {
          successMessage ?
            <div className="alert alert-success" role="alert">{successMessage}&nbsp;
            Go back and&nbsp;
              <Button variant={'link'} onClick={() => props.setComponent()} className={'link-in-success-message'}>
                run Monkey from the Island server </Button> to start AWS scan!</div>
            :
            ''
        }
        <Row className={'justify-content-center'}>
          <Col lg={4} md={6} sm={8} xs={12}>
            <Button className={'monkey-submit-button'} type={'submit'}>
              Submit
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
}
