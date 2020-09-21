import React from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import NextSelectionButton from '../../../ui-components/inline-selection/NextSelectionButton';
import {faCloud} from '@fortawesome/free-solid-svg-icons';
import AWSSetup from './AWSSetup';


const CloudOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {
      props.setComponent()
    }
  })
}

const getContents = (props) => {
  return (
    <>
      <NextSelectionButton title={'AWS'}
                           description={'Setup Amazon Web Services infrastructure scan.'}
                           icon={faCloud}
                           onButtonClick={() => {
                             props.setComponent(AWSSetup,
                               {setComponent: props.setComponent})
                           }}/>
    </>
  )
}

export default CloudOptions;
