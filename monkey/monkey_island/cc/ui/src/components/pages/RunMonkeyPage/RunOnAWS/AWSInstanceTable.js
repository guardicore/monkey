import React, {useState} from 'react';
import ReactTable from 'react-table'
import checkboxHOC from 'react-table/lib/hoc/selectTable';
import PropTypes from 'prop-types';


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

function AWSInstanceTable(props) {

  const [allToggled, setAllToggled] = useState(false);
  let checkboxTable = null;

  function toggleSelection(key) {
    key = key.replace('select-', '');
    // start off with the existing state
    let modifiedSelection = [...props.selection];
    const keyIndex = modifiedSelection.indexOf(key);
    // check to see if the key exists
    if (keyIndex >= 0) {
      // it does exist so we will remove it using destructing
      modifiedSelection = [
        ...modifiedSelection.slice(0, keyIndex),
        ...modifiedSelection.slice(keyIndex + 1)
      ];
    } else {
      // it does not exist so add it
      modifiedSelection.push(key);
    }
    // update the state
    props.setSelection(modifiedSelection);
  }

  function isSelected(key) {
    return props.selection.includes(key);
  }

  function toggleAll() {
    const selectAll = !allToggled;
    const selection = [];
    if (selectAll) {
      // we need to get at the internals of ReactTable
      const wrappedInstance = checkboxTable.getWrappedInstance();
      // the 'sortedData' property contains the currently accessible records based on the filter and sort
      const currentRecords = wrappedInstance.getResolvedState().sortedData;
      // we just push all the IDs onto the selection array
      currentRecords.forEach(item => {
        selection.push(item._original.instance_id);
      });
    }
    setAllToggled(selectAll);
    props.setSelection(selection);
  }

  function getTrProps(_, r) {
    let color = 'inherit';
    if (r) {
      let instId = r.original.instance_id;
      let runResult = getRunResults(instId);
      if (isSelected(instId)) {
        color = '#ffed9f';
      } else if (runResult) {
        color = runResult.status === 'error' ? '#f00000' : '#00f01b'
      }
    }

    return {
      style: {backgroundColor: color}
    };
  }

  function getRunResults(instanceId) {
    for(let result of props.results){
      if (result.instance_id === instanceId){
        return result
      }
    }
    return false
  }

  return (
    <div className="data-table-container">
      <CheckboxTable
        ref={r => (checkboxTable = r)}
        keyField="instance_id"
        columns={columns}
        data={props.data}
        showPagination={true}
        defaultPageSize={pageSize}
        className="-highlight"
        selectType="checkbox"
        toggleSelection={toggleSelection}
        isSelected={isSelected}
        toggleAll={toggleAll}
        selectAll={allToggled}
        getTrProps={getTrProps}
      />
    </div>
  );

}

AWSInstanceTable.propTypes = {
  data: PropTypes.arrayOf(PropTypes.exact({
    instance_id: PropTypes.string,
    name: PropTypes.string,
    os: PropTypes.string,
    ip_address: PropTypes.string
  })),
  results: PropTypes.arrayOf(PropTypes.string),
  selection: PropTypes.arrayOf(PropTypes.string),
  setSelection: PropTypes.func
}

export default AWSInstanceTable;
