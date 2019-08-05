import React, {Component} from "react";
import ReactTable from "react-table";

const columns = [
  {
    Header: 'Findings',
    columns: [
      { Header: 'Test', accessor: 'test'},
      { Header: 'Pillars', id: "pillars",
        accessor: x => {
          const pillars = x.pillars;
          const listItems = pillars.map((pillar) =>
            <li key={pillar}><span className="label label-warning" style={{margin: '2px'}}>{pillar}</span></li>
          );
          return <ul>{listItems}</ul>
        }
      },
      { Header: 'Events', id:"events", accessor: x => ZeroTrustReportFindingsTable.buildEventsComponent(x)}
    ]
  }
];

const pageSize = 10;

class ZeroTrustReportFindingsTable extends Component {
  render() {
    let defaultPageSize = this.props.findings.length > pageSize ? pageSize : this.props.findings.length;
    let showPagination = this.props.findings.length > pageSize;

    return (
      <div>
        <ReactTable
          columns={columns}
          data={this.props.findings}
          showPagination={showPagination}
          defaultPageSize={defaultPageSize}
        />
      </div>
    );
  }

  static buildEventsComponent(events) {
    return <button>Click to see events...</button>;
  }
}

export default ZeroTrustReportFindingsTable;
