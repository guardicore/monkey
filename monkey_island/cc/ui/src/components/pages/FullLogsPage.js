import React from 'react';
import {Col} from 'react-bootstrap';
import ReactJson from 'react-json-view'
import JSONTree from 'react-json-tree'
import ReactDataGrid, {Row} from 'react-data-grid';
import {Icon} from "react-fa";
const { Toolbar, Data: { Selectors } } = require('react-data-grid-addons');

// Custom Formatter component
const JsonCellFormatter = React.createClass({
  render() {
    return (
      <ReactJson src={this.props.value} collapsed={true} />
    );
  }
});

const RowRenderer = React.createClass({
  render() {
    return (
      <Row ref={ node => this.row = node } {...this.props}/>
    );
  }
  // height: '50px',
  //
  // onClick() {
  //   this.height = '200px';
  // },
  //
  // render() {
  //   return (
  //     <div style={{height: this.height}} onClick={this.onClick()}>
  //       <Icon name="expand" className="pull-right"/>
  //       <Row style={{minHeight: '100px'}} ref={ node => this.row = node } {...this.props}/>
  //     </div>
  //   );
  // }
});

class FullLogsPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ...this.getInitialState()
    };
  }

  getInitialState() {
    this._columns = [
      {
        key: 'telem_type',
        name: 'Type',
        width: 200,
        filterable: true,
        sortable: true
      },
      {
        key: 'monkey_guid',
        name: 'Monkey ID',
        filterable: true,
        sortable: true
      },
      {
        key: 'timestamp',
        name: 'Time',
        filterable: true,
        sortable: true
      },
      {
        key: 'data',
        name: 'More Info',
        formatter: JsonCellFormatter
      }
    ];

    return { rows: [], filters: {}, sortColumn: null, sortDirection: null };
  }

  getRandomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime())).toLocaleDateString();
  }

  getRows() {
    return Selectors.getRows(this.state);
  }

  getSize() {
    return this.getRows().length;
  }

  rowGetter = (rowIdx) => {
    const rows = this.getRows();
    return rows[rowIdx];
  };

  handleGridSort = (sortColumn, sortDirection) => {
    this.setState({ sortColumn: sortColumn, sortDirection: sortDirection });
  };

  handleFilterChange = (filter) => {
    let newFilters = Object.assign({}, this.state.filters);
    if (filter.filterTerm) {
      newFilters[filter.column.key] = filter;
    } else {
      delete newFilters[filter.column.key];
    }

    this.setState({ filters: newFilters });
  };

  onClearFilters = () => {
    this.setState({ filters: {} });
  };

  componentDidMount = () => {
    this.dataGrid.setState({canFilter: true}, () => this.hideFilterButton());
    fetch('/api/telemetry')
      .then(res => res.json())
      .then(res => this.setState({rows: res.objects}));
  };

  hideFilterButton = () => document.getElementsByClassName('react-grid-Toolbar')[0].style.display = 'none';

  render() {
    return (
      <Col xs={12}>
        <h1 className="page-title">Full Logs</h1>
        <div>
          <ReactDataGrid
            ref={(grid) => { this.dataGrid = grid; }}
            rowRenderer={RowRenderer}
            rowHeight={50}
            minHeight={500}
            columns={this._columns}
            toolbar={<Toolbar enableFilter={true}/>}
            rowGetter={this.rowGetter}
            rowsCount={this.getSize()}
            onGridSort={this.handleGridSort}
            onAddFilter={this.handleFilterChange}
            onClearFilters={this.onClearFilters} />
        </div>
      </Col>
    );
  }
}

export default FullLogsPageComponent;
