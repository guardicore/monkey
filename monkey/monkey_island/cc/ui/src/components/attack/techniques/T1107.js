import React from 'react';
import ReactTable from 'react-table';
import {renderMachineFromSystemData, ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1107 extends React.Component {

  constructor(props) {
    super(props);
  }

  static renderDelete(status) {
    if (status === ScanStatus.USED) {
      return <span>Yes</span>
    } else {
      return <span>No</span>
    }
  }

  static getDeletedFileColumns() {
    return ([{
      columns: [
        {
          Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x._id.machine),
          style: {'whiteSpace': 'unset'}
        },
        {Header: 'Path', id: 'path', accessor: x => x._id.path, style: {'whiteSpace': 'unset'}},
        {
          Header: 'Deleted?', id: 'deleted', accessor: x => this.renderDelete(x._id.status),
          style: {'whiteSpace': 'unset'}, width: 160
        }]
    }])
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.deleted_files.length !== 0 ?
          <ReactTable
            columns={T1107.getDeletedFileColumns()}
            data={this.props.data.deleted_files}
            showPagination={false}
            defaultPageSize={this.props.data.deleted_files.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1107;
