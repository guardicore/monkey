import React, {useEffect, useState, useCallback} from 'react';
import {nanoid} from 'nanoid';
import XDataGrid, {X_DATA_GRID_CLASSES} from '../XDataGrid';
import {GridRowEditStopReasons, GridRowModes} from '@mui/x-data-grid';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { Button } from '@mui/material';
import {
  getDataColumns, isAllValuesInRowAreEmpty,
  setErrorsForRow, trimRowValues
} from './credentialPairsHelper';

const getEmptyRow = () => {
  return [
    {
      id: nanoid(),
      identity: '',
      password: '',
      lm: '',
      ntlm: '',
      ssh_public_key: '',
      ssh_private_key: '',
      isNew: true
    }
  ]
}

const NewCredentialPair = (props) => {
  const {upsertRow} = {...props}

  const [rowModesModel, setRowModesModel] = useState({});
  const [rows, setRows] = useState(getEmptyRow());
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const newRowId = rows[0].id;
    setRowModesModel({...rowModesModel, [newRowId]: {mode: GridRowModes.Edit, fieldToFocus: 'identity'}});
  }, [rows?.[0]?.id]);

  const setErrorForRow = (rowId, isAddingError = true) => {
    setErrors((prevState) => {
        return setErrorsForRow(prevState, rowId, isAddingError)
      });
  }

  const handleAddRowClick = (id) => () => {
    setRowModesModel({...rowModesModel, [id]: {mode: GridRowModes.View}});
  };

  const processRowUpdate = useCallback(
    (newRow, oldRow) =>
      new Promise((resolve, reject) => {
        const newRowCopy = trimRowValues({...newRow});
        if(!isAllValuesInRowAreEmpty(newRowCopy)) {
          upsertRow(newRowCopy);
          setRows(getEmptyRow());
          resolve(newRowCopy);
        } else {
          setRows([{...oldRow}]);
          reject(oldRow);
        }
      }),
    []
  );

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const handleRowEditStop = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;
    }
  };

  return (
    <div>
      <XDataGrid
        columns={getDataColumns(null, true, setErrorForRow)}
        rows={rows}
        rowHeight={'25px'}
        showToolbar={false}
        maxHeight={'400px'}
        columnWidth={{min: 198, max: -1}}
        hideHeaders={false}
        processRowUpdate={processRowUpdate}
        onRowModesModelChange={handleRowModesModelChange}
        onRowEditStop={handleRowEditStop}
        editMode="row"
        rowModesModel={rowModesModel}
        onProcessRowUpdateError={()=>{void 0;}}
        getRowClassName={() => X_DATA_GRID_CLASSES.HIDDEN_LAST_EMPTY_CELL}
        className={'add-new-credentials-row'}
        setFlex={false}
      />
      <Button
        variant="contained"
        key={nanoid()}
        startIcon={<AddCircleIcon />}
        disabled={errors.includes(rows?.[0]?.id)}
        onClick={handleAddRowClick(rows?.[0]?.id)}>
        Save
      </Button>
   </div>
  );
}

export default NewCredentialPair;
