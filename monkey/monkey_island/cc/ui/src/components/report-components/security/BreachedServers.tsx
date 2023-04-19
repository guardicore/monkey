import React, {useEffect, useState} from 'react';
import ReactTable from 'react-table';
import {renderArray, renderIpAddresses} from '../common/RenderArrays';
import LoadingIcon from '../../ui-components/LoadingIcon';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';


const columns = [
  {
    Header: 'Breached Servers',
    columns: [
      {Header: 'Machine', accessor: 'label'},
      {
        Header: 'IP Addresses', id: 'ip_addresses',
        accessor: x => renderIpAddresses(x)
      },
      {Header: 'Exploits', id: 'exploits', accessor: x => renderArray(x.exploits)}
    ]
  }
];

const pageSize = 10;

function BreachedServersComponent() {

  const [exploitations, setExploitations] = useState(null);

  useEffect(() => {
    IslandHttpClient.get(APIEndpoint.monkey_exploitation, {}, true)
      .then(res => setExploitations(res.body['monkey_exploitations']))
  }, []);

  if(exploitations === null){
    return <LoadingIcon />
  }

  let defaultPageSize = exploitations.length > pageSize ? pageSize : exploitations.length;
  let showPagination = exploitations.length > pageSize;
  return (
    <>
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={exploitations}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    </>
  );

}

export default BreachedServersComponent;
