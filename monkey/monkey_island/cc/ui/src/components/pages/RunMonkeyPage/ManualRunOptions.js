import React, {useEffect, useState} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import LocalManualRunOptions from './LocalManualRunOptions';
import AuthComponent from '../../AuthComponent';
import {faLaptopCode} from '@fortawesome/free-solid-svg-icons/faLaptopCode';
import {faNetworkWired} from '@fortawesome/free-solid-svg-icons/faNetworkWired';
import {faCogs} from '@fortawesome/free-solid-svg-icons/faCogs';
import {Container} from 'react-bootstrap';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import {cloneDeep} from 'lodash';

function ManualRunOptions(props) {

  const [currentContent, setCurrentContent] = useState(loadingContents());
  const [ips, setIps] = useState([]);
  const [initialized, setInitialized] = useState(false);

  const authComponent = new AuthComponent({})

  useEffect(() => {
    if (initialized === false) {
      authComponent.authFetch('/api')
        .then(res => res.json())
        .then(res => {
          setIps([res['ip_addresses']][0]);
          setInitialized(true);
        });
    }
  })

  useEffect(() => {
    setCurrentContent(getDefaultContents());
  }, [initialized])

  function setComponent(component, props) {
    if (component === undefined) {
      setCurrentContent(getDefaultContents())
    } else {
      setCurrentContent(component({...props}))
    }
  }

  function loadingContents() {
    return (<div>Loading</div>)
  }

  function getDefaultContents() {
    const newProps = cloneDeep({...props, onBackButtonClick: props.disableManualOptions});
    return InlineSelection(defaultContents, newProps);
  }

  function defaultContents() {
    return (
      <>
        <NextSelectionButton text={'Local'}
                             description={'Run on a machine via command.'}
                             icon={faLaptopCode}
                             onButtonClick={() => {
                               setComponent(LocalManualRunOptions,
                                 {ips: ips, setComponent: setComponent})
                             }}/>
        <NextSelectionButton text={'Remote'}
                             description={'Run using remote command execution.'}
                             icon={faNetworkWired}
                             onButtonClick={() => {
                             }}/>
        <NextSelectionButton text={'Automation'}
                             description={'Run using automation tools like ansible or chef.'}
                             icon={faCogs}
                             onButtonClick={() => {
                             }}/>
      </>
    );
  }

  return currentContent;
}

export default ManualRunOptions;
