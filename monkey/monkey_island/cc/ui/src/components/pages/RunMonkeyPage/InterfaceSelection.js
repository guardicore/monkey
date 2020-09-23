import React from 'react';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import LocalManualRunOptions from './LocalManualRunOptions';

function InterfaceSelection(props) {
  return InlineSelection(getContents, props, LocalManualRunOptions)
}

const getContents = (props) => {
  const ips = props.ips.map((ip) =>
    <div key={ip}>{ip}</div>
  );
  return (<div>{ips}</div>);
}

export default InterfaceSelection;
