import React, {Component} from "react";
import ReactTable from "react-table";
import ZeroTrustPillars from "./ZeroTrustPillars";

class PillarLabel extends Component {
  render() {
    return <span className="label label-primary" style={{margin: '2px'}}>{this.props.pillar}</span>
  }
}

const columns = [
  {
    Header: 'Findings',
    columns: [
      { Header: 'Test', accessor: 'test',
        style: {'white-space': 'unset'}  // This enables word wrap
      },
      { Header: 'Pillars', id: "pillars",
        accessor: x => {
          const pillars = x.pillars;
          const listItems = pillars.map((pillar) =>
            <li key={pillar}><PillarLabel pillar={pillar}/></li>
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
