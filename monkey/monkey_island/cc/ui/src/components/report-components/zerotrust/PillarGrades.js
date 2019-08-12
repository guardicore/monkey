import React, {Component} from "react";
import {PillarLabel} from "./PillarLabel";
import PagenatedTable from "../common/PagenatedTable";

const columns = [
  {
    Header: 'Pillar Grading',
    columns: [
      { Header: 'Pillar', id: 'Pillar', accessor: x => {
          return (<PillarLabel pillar={x.Pillar} />);
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
    return <PagenatedTable data={this.props.pillars} columns={columns} pageSize={10}/>;
  }
}

export default PillarGrades;
