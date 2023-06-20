import React, {useEffect, useMemo} from 'react';
import PropTypes from 'prop-types';
import {DataGrid} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';


const columns = [
      {headerName: 'Machine', field: 'name'},
      {headerName: 'Instance ID', field: 'instance_id'},
      {headerName: 'IP Address', field: 'ip_address'},
      {headerName: 'OS', field: 'os'}
    ];

function getSelectedInstances(selectedRows, data) {
  let selectedInstances = [];
  for (let row of selectedRows) {
    let instance = data.find((inst) => { return inst['id'] === row; });
    selectedInstances.push(instance['instance_id']);
  }
  return selectedInstances;
}

function getSelectedRows(selectedInstances, data) {
  let selectedRows = [];
  for (let instance of selectedInstances) {
    let row = data.find((inst) => { return inst['instance_id'] === instance; });
    selectedRows.push(row['id']);
  }
  return selectedRows;
}

function AWSInstanceTable(props) {
  const [selectedRows, setSelectedRows] = React.useState([]);

  const data = useMemo(() => {
    return props.data.map((row) => {
      return {
        ...row,
        id: nanoid()
      };
    });
  } ,[props.data]);

  useEffect(() => {
    setSelectedRows(getSelectedRows(props.selection, data));
  }, [props.selection]);

  return (
    <div className="data-table-container">
      <DataGrid
        columns={columns}
        rows={data}
        pageSizeOptions={[10, 25, 50, 100]}
        getRowHeight={() => 'auto'}
        checkboxSelection
        disableRowSelectionOnClick
        onRowSelectionModelChange={(selectedRows) => {
          setSelectedRows(selectedRows);
          props.setSelection(getSelectedInstances(selectedRows, data));
        }}
        rowSelectionModel={selectedRows}
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
