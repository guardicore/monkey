import React from 'react';
import ReactTable from 'react-table';
import {getUsageColumns} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1035 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.services.length !== 0 ?
          <ReactTable
            columns={getUsageColumns()}
            data={this.props.data.services}
            showPagination={false}
            defaultPageSize={this.props.data.services.length}
          /> : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1035;
