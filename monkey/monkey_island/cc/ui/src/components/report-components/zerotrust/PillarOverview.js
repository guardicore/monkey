import React, {Component} from "react";
import PillarLabel from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";
import * as PropTypes from "prop-types";

const columns = [
  {
    Header: 'Pillar Grading',
    columns: [
      { Header: 'Pillar', id: 'Pillar', accessor: x => {
          return (<PillarLabel pillar={x.pillar.name} status={x.pillar.status} />);
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
    const data = this.props.grades.map((grade) => {
      const newGrade = grade;
      newGrade.pillar = {name: grade.pillar, status: this.props.pillarsToStatuses[grade.pillar]};
      return newGrade;
    });
    return (<div id={this.constructor.name}>
      <PaginatedTable data={data} columns={columns} pageSize={10}/>
    </div>);
  }
}

export default PillarOverview;

PillarOverview.propTypes = {
  grades: PropTypes.array,
  status: PropTypes.string,
};
