import React, {useEffect, useState} from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import NextSelectionButton from '../../../ui-components/inline-selection/NextSelectionButton';
import {faCheck, faCloud, faSync} from '@fortawesome/free-solid-svg-icons';
import AWSSetupOptions from './AWSConfiguration/AWSSetupOptions';
import {PROVIDERS} from './ProvidersEnum';
import AuthComponent from '../../../AuthComponent';


const CloudOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {
      props.setComponent()
    }
  })
}

const authComponent = new AuthComponent({})

const getContents = (props) => {

  const [description, setDescription] = useState('Loading...');
  const [iconType, setIconType] = useState('spinning-icon');
  const [icon, setIcon] = useState(faSync);

  useEffect(() => {
    authComponent.authFetch('/api/scoutsuite_auth/' + PROVIDERS.AWS)
      .then(res => res.json())
      .then(res => {
        if(res.is_setup){
          setDescription(getDescription(res.message));
          setIconType('icon-success');
          setIcon(faCheck);
        } else {
          setDescription('Setup Amazon Web Services infrastructure scan.');
          setIconType('')
          setIcon(faCloud);
        }
      });
  }, [props]);

  function getDescription(message){
    return (
      <>
        {message} Run <b>from the Island</b> to start the scan. Click next to change the configuration.
      </>
    )
  }

  return (
    <>
      <NextSelectionButton title={'AWS'}
                           description={description}
                           icon={icon}
                           iconType={iconType}
                           onButtonClick={() => {
                             props.setComponent(AWSSetupOptions,
                               {setComponent: props.setComponent})
                           }}/>
    </>
  )
}

export default CloudOptions;
