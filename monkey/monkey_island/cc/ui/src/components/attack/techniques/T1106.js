import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import { getUsageColumns } from "./Helpers"


class T1106 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.api_uses.length !== 0 ?
          <ReactTable
              columns={getUsageColumns()}
              data={this.props.data.api_uses}
              showPagination={false}
              defaultPageSize={this.props.data.api_uses.length}
          /> : ""}
      </div>
    );
  }
}

export default T1106;
