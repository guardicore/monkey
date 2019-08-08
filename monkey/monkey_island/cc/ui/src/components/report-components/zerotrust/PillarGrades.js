import React, {Component} from "react";
import ReactTable from "react-table";
import {PillarLabel} from "./PillarLabel";

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
    ]
  }
];

const pageSize = 10;

class PillarGrades extends Component {
  render() {
    if (this.props.pillars.length > 0) {
      let defaultPageSize = this.props.pillars.length > pageSize ? pageSize : this.props.pillars.length;
      let showPagination = this.props.pillars.length > pageSize;

      return (
        <div>
          <ReactTable
            columns={columns}
            data={this.props.pillars}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
          />
        </div>
      );
    }
    else { return (<div><pre>BAYAZ</pre></div>);}
  }
}

export default PillarGrades;
