import React from "react";
import PagenatedTable from "../common/PagenatedTable";
import AuthComponent from "../../AuthComponent";

const statusToIcon = {
  "Positive": "fa-shield alert-success",
  "Inconclusive": "fa-question alert-info",
  "Conclusive": "fa-unlock-alt alert-danger",
  "Unexecuted": "fa-toggle-off",
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
    return <PagenatedTable data={this.props.directivesStatus} columns={columns} pageSize={5}/>;
  }
}

export default DirectivesStatusTable;
