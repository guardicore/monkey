import React from 'react';
import ReactTable from 'react-table'
import checkboxHOC from 'react-table/lib/hoc/selectTable';

const CheckboxTable = checkboxHOC(ReactTable);

const columns = [
  {
    Header: 'Machines',
    columns: [
      {Header: 'Machine', accessor: 'name'},
      {Header: 'Instance ID', accessor: 'instance_id'},
      {Header: 'IP Address', accessor: 'ip_address'},
      {Header: 'OS', accessor: 'os'}
    ]
  }
];

const pageSize = 10;

class AwsRunTableComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selection: [],
      selectAll: false,
      result: {}
    }
  }

  toggleSelection = (key) => {
    // start off with the existing state
    let selection = [...this.state.selection];
    const keyIndex = selection.indexOf(key);
    // check to see if the key exists
    if (keyIndex >= 0) {
      // it does exist so we will remove it using destructing
      selection = [
        ...selection.slice(0, keyIndex),
        ...selection.slice(keyIndex + 1)
      ];
    } else {
      // it does not exist so add it
      selection.push(key);
    }
    // update the state
    this.setState({selection});
  };

  isSelected = key => {
    return this.state.selection.includes(key);
  };

  toggleAll = () => {
    const selectAll = !this.state.selectAll;
    const selection = [];
    if (selectAll) {
      // we need to get at the internals of ReactTable
      const wrappedInstance = this.checkboxTable.getWrappedInstance();
      // the 'sortedData' property contains the currently accessible records based on the filter and sort
      const currentRecords = wrappedInstance.getResolvedState().sortedData;
      // we just push all the IDs onto the selection array
      currentRecords.forEach(item => {
        selection.push(item._original.instance_id);
      });
    }
    this.setState({selectAll, selection});
  };

  getTrProps = (_, r) => {
    let color = 'inherit';
    if (r) {
      let instId = r.original.instance_id;
      if (this.isSelected(instId)) {
        color = '#ffed9f';
      } else if (Object.prototype.hasOwnProperty.call(this.state.result, instId)) {
        color = this.state.result[instId] ? '#00f01b' : '#f00000'
      }
    }

    return {
      style: {backgroundColor: color}
    };
  };

  render() {
    return (
      <div className="data-table-container">
        <CheckboxTable
          ref={r => (this.checkboxTable = r)}
          keyField="instance_id"
          columns={columns}
          data={this.props.data}
          showPagination={true}
          defaultPageSize={pageSize}
          className="-highlight"
          selectType="checkbox"
          toggleSelection={this.toggleSelection}
          isSelected={this.isSelected}
          toggleAll={this.toggleAll}
          selectAll={this.state.selectAll}
          getTrProps={this.getTrProps}
        />
      </div>
    );
  }
}

export default AwsRunTableComponent;
