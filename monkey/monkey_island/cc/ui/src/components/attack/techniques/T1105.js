import React from 'react';
import ReactTable from 'react-table';
import {ScanStatus} from './Helpers'


class T1105 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getFilesColumns() {
    return ([{
      Header: 'Files copied',
      columns: [
        {Header: 'Src. Machine', id: 'srcMachine', accessor: x => x.src, style: {'whiteSpace': 'unset'}, width: 170},
        {Header: 'Dst. Machine', id: 'dstMachine', accessor: x => x.dst, style: {'whiteSpace': 'unset'}, width: 170},
        {Header: 'Filename', id: 'filename', accessor: x => x.filename, style: {'whiteSpace': 'unset'}}
      ]
    }])
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status !== ScanStatus.UNSCANNED ?
          <ReactTable
            columns={T1105.getFilesColumns()}
            data={this.props.data.files}
            showPagination={false}
            defaultPageSize={this.props.data.files.length}
          /> : ''}
      </div>
    );
  }
}

export default T1105;
