import React from 'react';
import ReactTable from 'react-table';
import {getUsageColumns} from './Helpers'


class T1064 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.scripts.length !== 0 ?
          <ReactTable
            columns={getUsageColumns()}
            data={this.props.data.scripts}
            showPagination={false}
            defaultPageSize={this.props.data.scripts.length}
          /> : ''}
      </div>
    );
  }
}

export default T1064;
