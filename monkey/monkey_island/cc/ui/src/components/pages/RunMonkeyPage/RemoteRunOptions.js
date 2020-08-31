import React, {useEffect, useState} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import LocalManualRunOptions from './LocalManualRunOptions';
import {faLaptopCode} from '@fortawesome/free-solid-svg-icons/faLaptopCode';
import {faNetworkWired} from '@fortawesome/free-solid-svg-icons/faNetworkWired';
import {faCogs} from '@fortawesome/free-solid-svg-icons/faCogs';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import ManualRunOptions from './ManualRunOptions';


const RemoteRunOptions = (props) => {
  return InlineSelection(getContents, props)
}

function getContents() {
  return (
    <>
      <NextSelectionButton text={'Local'}
                           description={'Run on a machine via command.'}
                           icon={faLaptopCode}
                           onButtonClick={() => {
                             setComponent(LocalManualRunOptions,
                               {ips: ips, setComponent: setComponent})
                           }}/>
    </>
  );
}


export default ManualRunOptions;
