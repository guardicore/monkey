import React from 'react';
import PropTypes from 'prop-types';
import XDataGrid from '../../../ui-components/XDataGrid';

const columns = [
  {headerName: 'Machine', field: 'name'},
  {headerName: 'Instance ID', field: 'instance_id'},
  {headerName: 'IP Address', field: 'ip_address'},
  {headerName: 'OS', field: 'os'}
];

function AWSInstanceTable(props) {
  const {data, setSelection, selection, results} = {...props};

  const getRowBackgroundColor = (instanceId) => {
    if(instanceId) {
      let runResult = getRunResults(instanceId);
      if (!selection.includes(instanceId) && runResult) {
        if (runResult.status === 'error') {
          return 'run-error';
        } else {
          return 'run-success';
        }
      }
    }
    return null;
  }

  const getRunResults = (instanceId) => {
    for(let result of results){
      if (result.instance_id === instanceId){
        return result
      }
    }
    return false
  }

  const [rowSelectionModel, setRowSelectionModel] = React.useState(selection || []);

  const onRowsSelectionHandler = (newRowSelectionModel) => {
    setRowSelectionModel(newRowSelectionModel);
    setSelection(newRowSelectionModel);
  };

  return (
    <XDataGrid
      columns={columns}
      rows={data}
      showToolbar={false}
      checkboxSelection
      onRowSelectionModelChange={(newRowSelectionModel) => {onRowsSelectionHandler(newRowSelectionModel)}}
      rowSelectionModel={rowSelectionModel}
      getRowClassName={(params) => `x-data-grid-row ${getRowBackgroundColor(params.row.instance_id)}`}
    />
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
