import React, {Component} from "react";
import PillarLabel from "./PillarLabel";
import * as PropTypes from "prop-types";
import ResponsiveVennDiagram from "./VennDiagram";

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
    return (<div id={this.constructor.name}>
        <ResponsiveVennDiagram pillarsGrades={this.props.grades} />
    </div>);
  }
}

export default PillarOverview;

PillarOverview.propTypes = {
  grades: PropTypes.array,
};
