import React, {Component} from "react";
import PagenatedTable from "../common/PagenatedTable";

const columns = [
  {
    Header: 'Recommendations status',
    columns: [
      { Header: 'Recommendation', accessor: 'Recommendation',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      { Header: 'Status', id: "Status",
        accessor: x => {
          const statusToIcon = {
            "Positive": "fa-shield alert-success",
            "Inconclusive": "fa-question alert-info",
            "Conclusive": "fa-unlock-alt alert-danger",
            "Unexecuted": "fa-toggle-off",
          };
          return <i className={"fa " + statusToIcon[x.Status] + " fa-2x"} />;
        }
      },
      { Header: 'Tests', id:"Tests",
        accessor: x => {
          console.log(x.Tests);
          return <TestsStatus tests={x.Tests} />;
        }
      }
    ]
  }
];

class TestsStatus extends Component {
  render() {
    return (
      <pre>{JSON.stringify(this.props.tests,null,2)}</pre>
    );
  }
}

export class RecommendationsStatusTable extends Component {
  render() {
    return <PagenatedTable data={this.props.recommendationsStatus} columns={columns} pageSize={5}/>;
  }
}

export default RecommendationsStatusTable;
