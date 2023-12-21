import React, {useEffect, useState} from 'react';
import XDataGrid, {X_DATA_GRID_CLASSES} from '../XDataGrid';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import {Accordion, AccordionDetails, Typography} from '@mui/material';
import {GridActionsCellItem, GridRowEditStopReasons, GridRowModes} from '@mui/x-data-grid';
import {
  COLUMN_WIDTH,
  CREDENTIALS_ROW_KEYS,
  getDataColumns,
  IDENTITY_KEY,
  isAllValuesInRowAreEmpty,
  isRowDuplicated,
  setErrorsForRow,
  trimRowValues
} from './credentialPairsHelper';
import NewCredentialPair from './NewCredentialPair';
import {useStateCallback} from '../utils/useStateCallback';
import {nanoid} from 'nanoid';

const CredentialPairs = (props) => {
  const {onCredentialChange, credentials} = {...props};
  const [rowModesModel, setRowModesModel] = useStateCallback({});
  const [rows, setRows] = useStateCallback(credentials?.credentialsData || []);
  const [errors, setErrors] = useStateCallback([]);
  const [previousCredentialsId, setPreviousCredentialsId] = useState(credentials.id);
  const [showSecrets, setShowSecrets] = useState(false);

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
      }, () => onCredentialChange({credentialsData: [...rows], errors: [...errors]}));
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

    let isRowDuplicate = false;
    for (let existingRow of rows) {
      if (isRowDuplicated(newRow, existingRow)) {
        isRowDuplicate = true;
        break;
      }
    }

    if(!isRowEmpty && !isRowDuplicate) {
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

  const clearNewRowPropertyValue = (newRow, key) => {
    newRow[key] = '';
    return isAllValuesInRowAreEmpty(newRow, ['identity']);
  }

  const upsertRow = (newRow) => {
    let newRowCopy = {...newRow};
    let isNewRowFullyMerged = false;
    setRows((prevState) => {
        let foundDuplicatedRow = false;
        let newRowsArr = prevState.map(existingRow => {
          if (isRowDuplicated(newRowCopy, existingRow)) {
            foundDuplicatedRow = true;
          } else if (!foundDuplicatedRow && (existingRow.identity === newRowCopy.identity)) { // If the identity values match
            const mergedRow = {...existingRow}; // Create a copy of the existing row

            for (const key of CREDENTIALS_ROW_KEYS) {
              if (key !== IDENTITY_KEY) {
                if (mergedRow[key] === '') { // If the key is not identity and existing value is empty
                  mergedRow[key] = newRowCopy[key]; // Update the value in the merged row
                  if(newRowCopy[key]){
                    isNewRowFullyMerged = clearNewRowPropertyValue(newRowCopy, key);
                  }
                } else if (mergedRow[key] === newRowCopy[key]) {
                   isNewRowFullyMerged = clearNewRowPropertyValue(newRowCopy, key);
                }
              }
            }

            return mergedRow; // Return the merged row
          }

          return existingRow; // Return the existing row as is
        });

        if(!foundDuplicatedRow && !isAllValuesInRowAreEmpty(newRowCopy) && !isNewRowFullyMerged) {
          newRowsArr.push(newRowCopy);
        }

        return newRowsArr;
      },
      s => onCredentialChange({credentialsData: [...s], errors: [...errors]})
    );
  }

  const rowActionsHeaderComponent = <div className="secrets-visibility-button" onClick={() => setShowSecrets(prevState => !prevState)}>{showSecrets ?
    <VisibilityIcon/> : <VisibilityOffIcon/>}</div>;

  return (
    <div id="configure-propagation-credentials">
      <Typography variant="h5" component="h5">Credentials input</Typography>
      <Accordion expanded={true}>
        <AccordionDetails>
          <Typography>
            <NewCredentialPair upsertRow={upsertRow}/>
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Typography variant="h5" component="h5">Saved Credentials</Typography>
      <XDataGrid columns={getDataColumns(getRowActions, true, setErrorForRow, rowActionsHeaderComponent, showSecrets)}
                 rows={[...rows]}
                 rowHeight={'25px'}
                 showToolbar={false}
                 maxHeight={'400px'}
                 columnWidth={{min: COLUMN_WIDTH, max: -1}}
                 editMode="row"
                 rowModesModel={rowModesModel}
                 onRowModesModelChange={handleRowModesModelChange}
                 onRowEditStop={handleRowEditStop}
                 processRowUpdate={processRowUpdate}
                 onProcessRowUpdateError={()=>void(0)}
                 getRowClassName={() => X_DATA_GRID_CLASSES.HIDDEN_LAST_EMPTY_CELL}
                 className="configured-credentials"
                 setFlex={false}
      />
    </div>
  );
}

export default CredentialPairs;
