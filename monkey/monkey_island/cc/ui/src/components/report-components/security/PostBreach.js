import React from 'react';
import ReactTable from 'react-table';
import Pluralize from 'pluralize';
import {renderIpAddresses} from '../common/RenderArrays';
import parsePbaResults from './PostBreachParser';

let renderMachine = function (data) {
  return <div>{data.label} ( {renderIpAddresses(data)} )</div>
};

let renderPbaResults = function (results) {
  let pbaClass = '';
  if (results[1]) {
    pbaClass = 'pba-success'
  } else {
    pbaClass = 'pba-danger'
  }
  return <div className={pbaClass}> {results[0]} </div>
};

const subColumns = [
  {id: 'pba_name', Header: 'Name', accessor: x => x.name, style: {'whiteSpace': 'unset'}, width: 160},
  {id: 'pba_output', Header: 'Output', accessor: x => renderPbaResults(x.result), style: {'whiteSpace': 'unset'}}
];

let renderDetails = function (data) {
  let defaultPageSize = data.length > pageSize ? pageSize : data.length;
  let showPagination = data.length > pageSize;
  return <ReactTable
    data={data}
    columns={subColumns}
    defaultPageSize={defaultPageSize}
    showPagination={showPagination}
    style={{'backgroundColor': '#ededed'}}
  />
};

const columns = [
  {
    Header: 'Post breach actions',
    columns: [
      {id: 'pba_machine', Header: 'Machine', accessor: x => renderMachine(x)}
    ]
  }
];

const pageSize = 10;

class PostBreachComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let pbaMachines = this.props.data.filter(function (value) {
      return (value.pba_results !== 'None' && value.pba_results.length > 0);
    });
    pbaMachines = pbaMachines.map(pbaData => parsePbaResults(pbaData));
    let defaultPageSize = pbaMachines.length > pageSize ? pageSize : pbaMachines.length;
    let showPagination = pbaMachines > pageSize;
    const pbaCount = pbaMachines.reduce((accumulated, pbaMachine) => accumulated+pbaMachine['pba_results'].length, 0);
    return (
      <>
        <p>
          The Monkey performed <span
          className="badge badge-danger">{pbaCount}</span> post-breach {Pluralize('action', pbaCount)} on <span
          className="badge badge-warning">{pbaMachines.length}</span> {Pluralize('machine', pbaMachines.length)}:
        </p>
        <div className="data-table-container">
          <ReactTable
            columns={columns}
            data={pbaMachines}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
            SubComponent={row => {
              return renderDetails(row.original.pba_results);
            }}
          />
        </div>
      </>
    );
  }
}

export default PostBreachComponent;
