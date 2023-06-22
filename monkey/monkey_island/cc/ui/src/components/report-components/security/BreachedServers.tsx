import React, {useEffect, useState} from 'react';
import {renderArray, renderIpAddresses} from '../common/RenderArrays';
import LoadingIcon from '../../ui-components/LoadingIcon';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';
import XDataGrid, {XDataGridTitle} from '../../ui-components/XDataGrid';
import {nanoid} from 'nanoid';

const customToolbar = () => {
  return <XDataGridTitle title={'Breached Servers'} showDataActionsToolbar={false}/>;
}

const columns = [
  {headerName: 'Machine', field: 'label', sortable: false},
  {headerName: 'IP Addresses', field: 'ip_addresses', renderCell: ({value})=>{return value;}, sortable: false, flex: 1},
  {headerName: 'Exploits', field: 'exploits', renderCell: ({value})=>{return value;}, sortable: false}
];

// TODO: remove
// eslint-disable-next-line no-unused-vars
const mockData = [
  {id: nanoid(), label: 'label1', domain_name: '', ip_addresses: ['1.2.3', '4.5.6'], exploits: ['exploit1', 'exploit2', 'exploit23']},
  {id: nanoid(), label: 'label2', domain_name: 'domain', ip_addresses: ['120.130.140.150'], exploits: ['exploit4', 'exploit45']},
  {id: nanoid(), label: 'label3', domain_name: 'kuku or domain', ip_addresses: ['120.130.140.150', '192.168.1.1', '127.0.0.1'], exploits: ['exploit6', 'exploit66', 'ex90', 'ex 123']}
];

const prepareData = (exploitations) => {
  return exploitations.map((exploitation)=>{
    return {
      id: nanoid(),
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
      <XDataGrid
        toolbar={customToolbar}
        showToolbar={true}
        columns={columns}
        rows={exploitations}
      />
    </>
  );

}

export default BreachedServersComponent;
