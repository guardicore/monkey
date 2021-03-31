import React from 'react';
import InlineSelection from '../../../../ui-components/inline-selection/InlineSelection';
import NextSelectionButton from '../../../../ui-components/inline-selection/NextSelectionButton';
import {faKey, faTerminal} from '@fortawesome/free-solid-svg-icons';
import AWSCLISetup from './AWSCLISetup';
import CloudOptions from '../CloudOptions';
import AWSKeySetup from './AWSKeySetup';


const AWSSetupOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {
      props.setComponent(CloudOptions, props);
    }
  })
}

const getContents = (props) => {
  return (
    <>
      <NextSelectionButton title={'Security keys'}
                           description={'Provide security keys for monkey to authenticate.'}
                           icon={faKey}
                           onButtonClick={() => {
                             props.setComponent(AWSKeySetup,
                               {setComponent: props.setComponent})
                           }}/>
      <NextSelectionButton title={'AWS CLI'}
                           description={'Manually configure AWS CLI yourself.'}
                           icon={faTerminal}
                           onButtonClick={() => {
                             props.setComponent(AWSCLISetup,
                               {setComponent: props.setComponent})
                           }}/>
    </>
  )
}

export default AWSSetupOptions;
