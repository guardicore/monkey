import React, {useEffect, useState} from 'react';
import {renderArray, renderIpAddresses} from '../common/RenderArrays';
import LoadingIcon from '../../ui-components/LoadingIcon';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import XGrid, {XGridTitle} from '../../ui-components/XGrid';

const customToolbar = () => {
  return <XGridTitle title={'Breached Servers'} showDataActionsToolbar={false}/>;
}

const columns = [
  {headerName: 'Machine', field: 'label', sortable: false},
  {headerName: 'IP Addresses', field: 'ip_addresses', renderCell: ({value})=>{return value;}, sortable: false},
  {headerName: 'Exploits', field: 'exploits', renderCell: ({value})=>{return value;}, sortable: false}
];

const prepareData = (exploitations) => {
  return exploitations.map((exploitation)=>{
    return {
      label: exploitation?.label,
      ip_addresses: renderIpAddresses(exploitation),
      exploits: renderArray(exploitation?.exploits)
    }
  });
}

function BreachedServersComponent() {

  const [exploitations, setExploitations] = useState(null);

  useEffect(() => {
    IslandHttpClient.getJSON(APIEndpoint.monkey_exploitation, {}, true)
      .then(res => {
        setExploitations(prepareData(res.body['monkey_exploitations']));
      });
  }, []);

  if (exploitations === null) {
    return <LoadingIcon/>
  }

  return (
    <>
      <XGrid
        toolbar={customToolbar}
        showToolbar={true}
        columns={columns}
        data={exploitations}
      />
    </>
  );

}

export default BreachedServersComponent;
