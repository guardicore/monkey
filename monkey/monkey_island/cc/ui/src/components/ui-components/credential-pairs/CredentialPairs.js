import React, {useEffect, useState} from 'react';
import XDataGrid, {X_DATA_GRID_CLASSES} from '../XDataGrid';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import EditIcon from '@mui/icons-material/Edit';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DeleteIcon from '@mui/icons-material/Delete';
import {Accordion, AccordionDetails, AccordionSummary, Typography} from '@mui/material';
import {GridActionsCellItem, GridRowEditStopReasons, GridRowModes} from '@mui/x-data-grid';
import {
  COLUMN_WIDTH, CREDENTIALS_ROW_KEYS,
  getDataColumns, IDENTITY_KEY,
  isAllValuesInRowAreEmpty,
  isRowDuplicated,
  setErrorsForRow, trimRowValues
} from './credentialPairsHelper';
import NewCredentialPair from './NewCredentialPair';
import {useStateCallback} from '../utils/useStateCallback';
import {nanoid} from 'nanoid';

const initialState = {
  sorting: {
    sortModel: [{field: 'identity', sort: 'asc'}]
  }
};

const CredentialPairs = (props) => {
  const {onCredentialChange, credentials} = {...props};
  const [rowModesModel, setRowModesModel] = useStateCallback({});
  const [rows, setRows] = useStateCallback(credentials?.credentialsData || []);
  const [errors, setErrors] = useStateCallback([]);
  const [previousCredentialsId, setPreviousCredentialsId] = useState(credentials.id);

  useEffect(() => {
    if (previousCredentialsId !== credentials.id) {
      setRows(credentials.credentialsData);
      setPreviousCredentialsId(credentials.id);
    }
  });

  const setErrorForRow = (rowId, isAddingError = true) => {
    setErrors((prevState) => {
        return setErrorsForRow(prevState, rowId, isAddingError)
      },
      s => onCredentialChange({credentialsData: [...rows], errors: [...s]})
    );
  }

  const getRowActions = (rowId) => {
    const isInEditMode = rowModesModel[rowId]?.mode === GridRowModes.Edit;

    if (isInEditMode) {
      return [
        <GridActionsCellItem
          key={nanoid()}
          icon={<SaveIcon/>}
          label="Save"
          sx={{
            color: 'primary.main'
          }}
          disabled={errors.includes(rowId)}
          onClick={handleSaveClick(rowId)}
        />,
        <GridActionsCellItem
          key={nanoid()}
          icon={<CancelIcon/>}
          label="Cancel"
          className="textPrimary"
          onClick={handleCancelClick(rowId)}
          color="inherit"
        />
      ];
    }

    return [
      <GridActionsCellItem
        key={nanoid()}
        icon={<EditIcon/>}
        label="Edit"
        className="textPrimary"
        onClick={handleEditClick(rowId)}
        color="inherit"
      />,
      <GridActionsCellItem
        key={nanoid()}
        icon={<DeleteIcon/>}
        label="Delete"
        onClick={handleDeleteClick(rowId)}
        color="inherit"
      />
    ];
  }

  const handleRowEditStop = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;
    }
  };

  const handleEditClick = (id) => () => {
    setRowModesModel({...rowModesModel, [id]: {mode: GridRowModes.Edit}});
  };

  const handleSaveClick = (id) => () => {
    if (!errors.includes(id)) {
      setRowModesModel({
        ...rowModesModel,
        [id]: {mode: GridRowModes.View}
      }, s => onCredentialChange({credentialsData: [...rows], errors: [...errors]}));
    }
  };

  const handleDeleteClick = (id) => () => {
    setRows(rows.filter((row) => row.id !== id),
      s => onCredentialChange({credentialsData: [...s], errors: [...errors]}));
  };

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: {mode: GridRowModes.View, ignoreModifications: true}
    });

    setErrors(errors.filter((rowId) => rowId !== id), s => onCredentialChange({
      credentialsData: [...rows],
      errors: [...s]
    }));
  };

  const processRowUpdate = (newRow) => {
    const updatedRow = trimRowValues({...newRow, isNew: false});
    const isRowEmpty = isAllValuesInRowAreEmpty(updatedRow);
    if(!isRowEmpty) {
      setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)), s => onCredentialChange({
        credentialsData: [...s],
        errors: [...errors]
      }));
    }
    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const upsertRow = (newRow) => {
    let newRowCopy = {...newRow};
    let isNewRowMerged = false;
    setRows((prevState) => {
        let foundDuplicatedRow = false;
        let newRowsArr = prevState.map(existingRow => {
          if (isRowDuplicated(newRowCopy, existingRow)) {
            foundDuplicatedRow = true;
          } else if (existingRow.identity === newRowCopy.identity) { // If the identity values match
            const mergedRow = {...existingRow}; // Create a copy of the existing row

            for (const key of CREDENTIALS_ROW_KEYS) {
              if (key !== IDENTITY_KEY) {
                if (mergedRow[key] === '') { // If the key is not identity and existing value is empty
                  mergedRow[key] = newRowCopy[key]; // Update the value in the merged row
                  if(newRowCopy[key]){
                    isNewRowMerged = true;
                  }
                  newRowCopy[key] = ''; // Update the value in the new row to empty
                } else if (mergedRow[key] === newRowCopy[key]) {
                  newRowCopy[key] = '';
                }
              }
            }

            return mergedRow; // Return the merged row
          }

          return existingRow; // Return the existing row as is
        });

        if (!foundDuplicatedRow && !isAllValuesInRowAreEmpty(newRowCopy) && !isNewRowMerged) { // If new row has non-empty values and not duplicated
          newRowsArr.push(newRowCopy); // Insert the new row to the merged rows array
        }

        return newRowsArr;
      },
      s => onCredentialChange({credentialsData: [...s], errors: [...errors]})
    );
  }

  return (
    <div id="configure-propagation-credentials">
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon/>}
          aria-controls="new-credential-pairs-content"
          id="new-credential-pairs-panel"
        >
          <Typography>ADD NEW CREDENTIALS</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            <NewCredentialPair upsertRow={upsertRow}/>
          </Typography>
        </AccordionDetails>
      </Accordion>

      <XDataGrid columns={getDataColumns(getRowActions, false, setErrorForRow)}
                 rows={[...rows]}
                 rowHeight={'25px'}
                 showToolbar={false}
                 maxHeight={'400px'}
                 columnWidth={{min: COLUMN_WIDTH, max: COLUMN_WIDTH}}
                 editMode="row"
                 rowModesModel={rowModesModel}
                 onRowModesModelChange={handleRowModesModelChange}
                 onRowEditStop={handleRowEditStop}
                 processRowUpdate={processRowUpdate}
                 getRowClassName={() => X_DATA_GRID_CLASSES.HIDDEN_LAST_EMPTY_CELL}
                 className="configured-credentials"
                 initialState={initialState}
      />
    </div>
  );
}

export default CredentialPairs;
