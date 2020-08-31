import React from 'react';
import ReactTable from 'react-table'
import {renderArray} from '../common/RenderArrays';


const columns = [
  {
    Header: 'Powerful Users',
    columns: [
      {Header: 'Username', accessor: 'username'},
      {Header: 'Machines', id: 'machines', accessor: x => renderArray(x.machines)},
      {Header: 'Services', id: 'services', accessor: x => renderArray(x.services_names)}
    ]
  }
];

const pageSize = 10;

class StrongUsersComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let defaultPageSize = this.props.data.length > pageSize ? pageSize : this.props.data.length;
    let showPagination = this.props.data.length > pageSize;
    return (
      <div className="data-table-container">
        <ReactTable
          columns={columns}
          data={this.props.data}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    );
  }
}

export default StrongUsersComponent;
