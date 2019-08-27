import React, {Fragment} from "react";
import PaginatedTable from "../common/PaginatedTable";
import AuthComponent from "../../AuthComponent";
import 'styles/ZeroTrustPillars.css'
import StatusLabel from "./StatusLabel";
import * as PropTypes from "prop-types";


const columns = [
  {
    columns: [
      { Header: 'Status', id: 'status',
        accessor: x => {
          return <StatusLabel status={x.status} size="fa-3x" showText={false} />;
        },
        maxWidth: 80
      },
      { Header: 'Directive', accessor: 'directive',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      { Header: 'Tests', id: 'tests',
        style: {'whiteSpace': 'unset'},  // This enables word wrap
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
        {this.getFilteredTestsByStatusIfAny(conclusiveStatus)}
        {this.getFilteredTestsByStatusIfAny(inconclusiveStatus)}
        {this.getFilteredTestsByStatusIfAny(positiveStatus)}
        {this.getFilteredTestsByStatusIfAny(unexecutedStatus)}
      </Fragment>
    );
  }

  getFilteredTestsByStatusIfAny(statusToFilter) {
    const filteredTests = this.props.tests.filter((test) => {
        return (test.status === statusToFilter);
      }
    );

    if (filteredTests.length > 0) {
      const listItems = filteredTests.map((test) => {
        return (<li key={test.test}>{test.test}</li>)
      });
      return <Fragment>
        <StatusLabel status={statusToFilter} showText={false}/>
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

DirectivesStatusTable.propTypes = {directivesStatus: PropTypes.array};
