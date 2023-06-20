import React, {useEffect, useState} from 'react';
import AuthComponent from '../../../AuthComponent';
import '../../../../styles/components/RunOnIslandButton.scss';
import {faCloud} from '@fortawesome/free-solid-svg-icons';
import AWSRunOptions from './AWSRunOptions';
import NextSelectionButton from '../../../ui-components/inline-selection/NextSelectionButton';
import {Alert, Button} from 'react-bootstrap';
import LoadingIcon from '../../../ui-components/LoadingIcon';


function AWSRunButton(props) {

  const authComponent = new AuthComponent({});

  const [isOnAWS, setIsOnAWS] = useState(false);
  const [AWSInstances, setAWSInstances] = useState([]);
  const [awsMachineCollectionError, setAwsMachineCollectionError] = useState('');
  const [componentLoading, setComponentLoading] = useState(true);

  useEffect(() => {
    checkIsOnAWS();
  }, []);

  function checkIsOnAWS() {
    // TODO: Revert these changes
    setComponentLoading(false);
    setIsOnAWS(true);
    setAwsMachineCollectionError('');
    setAWSInstances([{'instance_id': 'instance_id-1', 'os': 'linux'}, {'instance_id': 'instance_id-2', 'os': 'windows'}]);
    // authComponent.authFetch('/api/remote-monkey?action=list_aws', {}, true)
    //   .then(res => res.json())
    //   .then(res => {
    //     let isAws = res['is_aws'];
    //     setComponentLoading(false);
    //     if (isAws) {
    //       // On AWS!
    //       // Checks if there was an error while collecting the aws machines.
    //       let isErrorWhileCollectingAwsMachines = (res['error'] != null);
    //       if (isErrorWhileCollectingAwsMachines) {
    //         // There was an error. Finish loading, and display error message.
    //         setIsOnAWS(true);
    //         setAwsMachineCollectionError(res['error']);
    //       } else {
    //         // No error! Finish loading and display machines for user
    //         setIsOnAWS(true);
    //         setAWSInstances(res['instances']);
    //       }
    //     }
    //   });
  }

  function getAWSButton() {
    return <NextSelectionButton title={'AWS run'}
                                description={'Run on a chosen AWS instance in the cloud.'}
                                icon={faCloud}
                                onButtonClick={() => {
                                  props.setComponent(AWSRunOptions,
                                    {AWSInstances: AWSInstances, setComponent: props.setComponent})
                                }}/>
  }

  function getErrorDisplay() {
    return (
    <Alert variant={'info'}>Detected ability to run on different AWS instances.
      To enable this feature, follow the &nbsp;
      <Button variant={'link'} className={'inline-link'}
              href={'https://techdocs.akamai.com/infection-monkey/docs/running-the-monkey-on-aws-ec2-instances/'}>
        Tutorial
      </Button> and refresh the page. Error received while trying to list AWS instances: {awsMachineCollectionError}
    </Alert> );
  }

  let displayed = '';
  if (componentLoading) {
    displayed = LoadingIcon();
  }
  if (awsMachineCollectionError !== '') {
    displayed = getErrorDisplay();
  } else if (isOnAWS) {
    displayed = getAWSButton();
  }

  return displayed;
}

export default AWSRunButton;
