import React, {Fragment} from 'react';
import PaginatedTable from '../common/PaginatedTable';
import AuthComponent from '../../AuthComponent';
import StatusLabel from './StatusLabel';
import * as PropTypes from 'prop-types';
import {ZeroTrustStatuses} from './ZeroTrustPillars';


const MAX_WIDTH_STATUS_COLUMN = 80;
const columns = [
  {
    columns: [
      {
        Header: 'Status', id: 'status',
        accessor: x => {
          return <StatusLabel status={x.status} size="3x" showText={false}/>;
        },
        maxWidth: MAX_WIDTH_STATUS_COLUMN
      },
      {
        Header: 'Zero Trust Principle', accessor: 'principle',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      {
        Header: 'Monkey Tests', id: 'tests',
        style: {'whiteSpace': 'unset'},  // This enables word wrap
        accessor: x => {
          return <TestsStatus tests={x.tests}/>;
        }
      }
    ]
  }
];

class TestsStatus extends AuthComponent {
  render() {
    return (
      <Fragment>
        {this.getFilteredTestsByStatusIfAny(ZeroTrustStatuses.failed)}
        {this.getFilteredTestsByStatusIfAny(ZeroTrustStatuses.verify)}
        {this.getFilteredTestsByStatusIfAny(ZeroTrustStatuses.passed)}
        {this.getFilteredTestsByStatusIfAny(ZeroTrustStatuses.unexecuted)}
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

export class PrinciplesStatusTable extends AuthComponent {
  render() {
    return <PaginatedTable data={this.props.principlesStatus} columns={columns} pageSize={5}/>;
  }
}

export default PrinciplesStatusTable;

PrinciplesStatusTable.propTypes = {principlesStatus: PropTypes.array};
