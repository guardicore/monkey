import React from "react";
import PaginatedTable from "../common/PaginatedTable";
import AuthComponent from "../../AuthComponent";
import 'styles/ZeroTrustPillars.css'

const statusToIcon = {
  "Positive": "fa-clipboard-check status-success",
  "Inconclusive": "fa-exclamation-triangle status-warning",
  "Conclusive": "fa-bomb status-danger",
  "Unexecuted": "fa-question status-default",
};

const columns = [
  {
    Header: 'Directives status',
    columns: [
      { Header: 'Directive', accessor: 'directive',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      { Header: 'Status', id: 'status',
        accessor: x => {
          return <i className={"fa " + statusToIcon[x.status] + " fa-3x"} />;
        }
      },
      { Header: 'Tests', id: 'tests',
        accessor: x => {
          return <TestsStatus tests={x.tests} />;
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
        return (test.status === statusToFilter);
      }
    );

    if (filteredTests.length > 0) {
      const listItems = filteredTests.map((test) => {
        return (<li key={test.test}>{test.test}</li>)
      });
      return <div><i className={"fa " + statusToIcon[statusToFilter]}/> {statusToFilter}<ul>{listItems}</ul></div>;
    }
    return <div/>;
  }
}

export class DirectivesStatusTable extends AuthComponent {
  render() {
    return <PaginatedTable data={this.props.directivesStatus} columns={columns} pageSize={5}/>;
  }
}

export default DirectivesStatusTable;
