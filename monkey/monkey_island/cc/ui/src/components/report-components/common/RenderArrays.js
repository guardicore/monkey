import React from 'react';

export let renderArray = function (val) {
    return <>{val.map(x => <div key={x}>{x}</div>)}</>;
};
export let renderIpAddresses = function (val) {
    return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? ' ('.concat(val.domain_name, ')') : '')} </div>;
};
