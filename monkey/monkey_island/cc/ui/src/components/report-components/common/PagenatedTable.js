import React, {Component} from "react";
import ReactTable from "react-table";

class PagenatedTable extends Component {
  render() {
    if (this.props.data.length > 0) {
      let defaultPageSize = this.props.data.length > this.props.pageSize ? this.props.pageSize : this.props.data.length;
      let showPagination = this.props.data.length > this.props.pageSize;

      return (
        <div>
          <ReactTable
            columns={this.props.columns}
            data={this.props.data}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
          />
        </div>
      );
    }
    else {
      return (
        <div/>
      );
    }
  }
}

export default PagenatedTable;
