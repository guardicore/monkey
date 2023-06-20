import React from 'react';
import PropTypes from 'prop-types';
import XGrid from '../../../ui-components/XGrid';


const columns = [
  {headerName: 'Machine', field: 'name'},
  {headerName: 'Instance ID', field: 'instance_id'},
  {headerName: 'IP Address', field: 'ip_address'},
  {headerName: 'OS', field: 'os'}
];

function AWSInstanceTable(props) {

  // const [allToggled, setAllToggled] = useState(false);
  // let checkboxTable = null;
  //
  // function toggleSelection(key) {
  //   // key = key.replace('select-', '');
  //   // start off with the existing state
  //   let modifiedSelection = [...props.selection];
  //   const keyIndex = modifiedSelection.indexOf(key);
  //   // check to see if the key exists
  //   if (keyIndex >= 0) {
  //     // it does exist so we will remove it using destructing
  //     modifiedSelection = [
  //       ...modifiedSelection.slice(0, keyIndex),
  //       ...modifiedSelection.slice(keyIndex + 1)
  //     ];
  //   } else {
  //     // it does not exist so add it
  //     modifiedSelection.push(key);
  //   }
  //   // update the state
  //   props.setSelection(modifiedSelection);
  // }
  //
  // function isSelected(key) {
  //   return props.selection.includes(key);
  // }
  //
  // function toggleAll() {
  //   const selectAll = !allToggled;
  //   const selection = [];
  //   if (selectAll) {
  //     // we need to get at the internals of ReactTable
  //     const wrappedInstance = checkboxTable.getWrappedInstance();
  //     // the 'sortedData' property contains the currently accessible records based on the filter and sort
  //     const currentRecords = wrappedInstance.getResolvedState().sortedData;
  //     // we just push all the IDs onto the selection array
  //     currentRecords.forEach(item => {
  //       selection.push(item._original.instance_id);
  //     });
  //   }
  //   setAllToggled(selectAll);
  //   props.setSelection(selection);
  // }
  //
  // function getTrProps(_, r) {
  //   let color = 'inherit';
  //   if (r) {
  //     let instId = r.original.instance_id;
  //     let runResult = getRunResults(instId);
  //     if (isSelected(instId)) {
  //       color = '#ffed9f';
  //     } else if (runResult) {
  //       color = runResult.status === 'error' ? '#f00000' : '#00f01b'
  //     }
  //   }
  //
  //   return {
  //     style: {backgroundColor: color}
  //   };
  // }
  //
  // function getRunResults(instanceId) {
  //   for(let result of props.results){
  //     if (result.instance_id === instanceId){
  //       return result
  //     }
  //   }
  //   return false
  // }
  const [rowSelectionModel, setRowSelectionModel] = React.useState([]);

  return (
    <XGrid
      columns={columns}
      rows={props.data}
      checkboxSelection
      onRowSelectionModelChange={(newRowSelectionModel) => {
        setRowSelectionModel(newRowSelectionModel);
        props.setSelection(rowSelectionModel);
      }}
      rowSelectionModel={rowSelectionModel}
    />

    // <div className="data-table-container">
    //   <CheckboxTable
    //     ref={r => (checkboxTable = r)}
    //     keyField="instance_id"
    //     columns={columns}
    //     data={props.data}
    //     showPagination={true}
    //     defaultPageSize={pageSize}
    //     className="-highlight"
    //     selectType="checkbox"
    //     toggleSelection={toggleSelection}
    //     isSelected={isSelected}
    //     toggleAll={toggleAll}
    //     selectAll={allToggled}
    //     getTrProps={getTrProps}
    //   />
    // </div>
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
