import React, {useEffect, useState} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import LocalManualRunOptions from './LocalManualRunOptions';
import AuthComponent from '../../AuthComponent';
import BackButton from '../../ui-components/inline-selection/BackButton';

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
    return (
      <div className={`container inline-selection-component`}>
        <NextSelectionButton text={'Local'} onButtonClick={() => {
          setComponent(LocalManualRunOptions, {ips: ips, setComponent: setComponent})
        }}/>
        <NextSelectionButton text={'Remote'} onButtonClick={() => {
        }}/>
        <NextSelectionButton text={'Automation'} onButtonClick={() => {
        }}/>
        <BackButton onClick={props.disableManualOptions} />
      </div>
    );
  }

  return currentContent;
}

export default ManualRunOptions;
