import React, {Component} from "react";
import {PillarLabel} from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";
import {PillarsSummary} from "./PillarsSummary";

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

class PillarOverview extends Component {
  render() {
    return (<div id={this.constructor.name}>
      <PillarsSummary pillars={this.props.pillars.summary}/>
      <br/>
      <PaginatedTable data={this.props.pillars.grades} columns={columns} pageSize={10}/>
    </div>);
  }
}

export default PillarOverview;
