import React, {Component} from "react";
import {PillarLabel} from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";

const columns = [
  {
    Header: 'Pillar Grading',
    columns: [
      { Header: 'Pillar', id: 'Pillar', accessor: x => {
          return (<PillarLabel pillar={x.pillar} />);
        }},
      { Header: 'Conclusive', accessor: 'Conclusive'},
      { Header: 'Inconclusive', accessor: 'Inconclusive'},
      { Header: 'Unexecuted', accessor: 'Unexecuted'},
      { Header: 'Positive', accessor: 'Positive'},
    ]
  }
];

class PillarGrades extends Component {
  render() {
    return <PaginatedTable data={this.props.pillars} columns={columns} pageSize={10}/>;
  }
}

export default PillarGrades;
