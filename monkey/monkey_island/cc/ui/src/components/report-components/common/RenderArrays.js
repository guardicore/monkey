import React from 'react';

export let renderArray = function (val, className='') {
    return <>{val.map(x => <div key={x} className={className}>{x}</div>)}</>;
};
export let renderIpAddresses = function (val) {
    return <div>
      {renderArray(val.ip_addresses, 'ip-address')} {(val.domain_name ? ' ('.concat(val.domain_name, ')') : '')}
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
