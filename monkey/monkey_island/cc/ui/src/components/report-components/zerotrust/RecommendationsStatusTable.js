import React, {Component} from "react";
import PagenatedTable from "../common/PagenatedTable";
import AuthComponent from "../../AuthComponent";

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
          return <TestsStatus tests={x.Tests} />;
        }
      }
    ]
  }
];

class TestsStatus extends AuthComponent {
  render() {
    const positiveStatus = "Positive";
    const conclusiveStatus = "Conclusive";
    const inconclusiveStatus = "Inconclusive";
    const unexecutedStatus = "Unexecuted";

    return (
      <div>
        {this.getTestsOfStatusIfAny(conclusiveStatus)}
        {this.getTestsOfStatusIfAny(inconclusiveStatus)}
        {this.getTestsOfStatusIfAny(positiveStatus)}
        {this.getTestsOfStatusIfAny(unexecutedStatus)}
      </div>
    );
  }

  getTestsOfStatusIfAny(statusToFilter) {
    const filteredTests = this.props.tests.filter((test) => {
        return (test.Status === statusToFilter);
      }
    );

    if (filteredTests.length > 0) {
      const listItems = filteredTests.map((test) => {
        return (<li key={test.Test}>{test.Test}</li>)
      });
      return <div>{statusToFilter}<ul>{listItems}</ul></div>;
    }
    return <div/>;
  }
}

export class RecommendationsStatusTable extends AuthComponent {
  render() {
    return <PagenatedTable data={this.props.recommendationStatus} columns={columns} pageSize={5}/>;
  }
}

export default RecommendationsStatusTable;
