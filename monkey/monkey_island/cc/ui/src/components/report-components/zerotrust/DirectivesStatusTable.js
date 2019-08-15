import React, {Fragment} from "react";
import PaginatedTable from "../common/PaginatedTable";
import AuthComponent from "../../AuthComponent";
import 'styles/ZeroTrustPillars.css'
import {StatusLabel} from "./StatusLabel";



const columns = [
  {
    Header: 'Directives status',
    columns: [
      { Header: 'Directive', accessor: 'directive',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      { Header: 'Status', id: 'status',
        accessor: x => {
          return <StatusLabel status={x.status} size="fa-3x" showText={false} />;
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
      <Fragment>
        {this.getTestsOfStatusIfAny(conclusiveStatus)}
        {this.getTestsOfStatusIfAny(inconclusiveStatus)}
        {this.getTestsOfStatusIfAny(positiveStatus)}
        {this.getTestsOfStatusIfAny(unexecutedStatus)}
      </Fragment>
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
      return <Fragment>
        <StatusLabel status={statusToFilter} showText={true}/>
        <ul>{listItems}</ul>
      </Fragment>;
    }
    return <Fragment/>;
  }
}

export class DirectivesStatusTable extends AuthComponent {
  render() {
    return <PaginatedTable data={this.props.directivesStatus} columns={columns} pageSize={5}/>;
  }
}

export default DirectivesStatusTable;
