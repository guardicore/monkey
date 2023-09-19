import React from 'react';

export let renderArray = function (val, className='') {
    return <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'flex-start'}}>
      {val.map(x => <div key={x} className={className}>{x}</div>)}
    </div>;
};
export let renderIpAddresses = function (val) {
    return <div style={{display: 'flex', width: '100%', gap: '0.875rem'}}>
      {renderArray(val.ip_addresses, 'ip-address')}
      {(!!val?.domain_name) && <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>{val.domain_name}</div>}
    </div>;
};

export let renderMachineArray = function(array) {
  return <>{array.map(x => <div key={x.network_interfaces[0]}>{x.network_interfaces[0]}</div>)}</>;
}

export let renderLimitedArray = function (array,
                                          limit,
                                          className='',
                                          separator=',') {
  let elements = [];
  if(array.length < limit){
    limit = array.length;
  }
  for(let i = 0; i < limit; i++){
    let element = '';
    if(i !== 0) {
      element = (<>{separator} {array[i]}</>);
    } else {
      element = (<>{array[i]}</>);
    }
    elements.push(<div className={className} key={array[i]}>{element}</div>);
  }
  let remainder = array.length - limit;
  if(remainder > 0){
    elements.push(<div className={className} key={'remainder'}>
      &nbsp;and {remainder} more
    </div>);
  }
  return elements
}
