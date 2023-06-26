// eslint-disable-next-line no-unused-vars
import React, {useEffect, useState} from 'react';
import XDataGrid from './XDataGrid';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {Accordion, AccordionDetails, AccordionSummary, Typography} from '@mui/material';
import {GridActionsCellItem, GridRowEditStopReasons, GridRowModes} from '@mui/x-data-grid';
import {nanoid} from 'nanoid';

const getMainColumns = () => {
  return [
    {headerName: 'Identity', field: 'identity', editable: true},
    {headerName: 'Password', field: 'password', editable: true},
    {headerName: 'LM', field: 'lm', editable: true},
    {headerName: 'NTLM', field: 'ntlm', editable: true},
    {headerName: 'SSH Public key', field: 'ssh_public_key', editable: true},
    {headerName: 'SSH Private key', field: 'ssh_private_key', editable: true}
  ];
}

const mockRows = [
  {
    id: nanoid(),
    identity: 'kuku',
    password: '1234',
    lm: '1234',
    ntlm: '1234',
    ssh_public_key: 'oihsfdiowfdiow',
    ssh_private_key: 'kjwefkefdkewf'
  },
  {
    id: nanoid(),
    identity: 'me_me',
    password: '1234',
    lm: '1234',
    ntlm: '1234',
    ssh_public_key: 'oihsfdiowfdiow',
    ssh_private_key: 'kjwefkefdkewf'
  },
  {
    id: nanoid(),
    identity: 'youyou',
    password: '1234',
    lm: '1234',
    ntlm: '1234',
    ssh_public_key: 'oihsfdiowfdiow',
    ssh_private_key: 'kjwefkefdkewf'
  }
];

const newRowColumns = getMainColumns();

const updateFilterAndSortPropertiesToColumn = (col, filterable = true, sortable = true) => {
  const colObj = {...col};
  colObj['filterable'] = filterable;
  colObj['sortable'] = sortable;
  return colObj;
}

// eslint-disable-next-line no-unused-vars
const CredentialPairs = () => {
  const [rowModesModel, setRowModesModel] = useState({});
  const [rows, setRows] = useState(mockRows);

  useEffect(() => {
    console.log(rowModesModel);
  }, [rowModesModel])

  // eslint-disable-next-line no-unused-vars
  const getRowActions = (rowId) => {
    const isInEditMode = rowModesModel[rowId]?.mode === GridRowModes.Edit;

    if (isInEditMode) {
      return [
        // eslint-disable-next-line react/jsx-key
        <GridActionsCellItem
          icon={<SaveIcon/>}
          label="Save"
          sx={{
            color: 'primary.main'
          }}
          onClick={handleSaveClick(rowId)}
        />,
        // eslint-disable-next-line react/jsx-key
        <GridActionsCellItem
          icon={<CancelIcon/>}
          label="Cancel"
          className="textPrimary"
          onClick={handleCancelClick(rowId)}
          color="inherit"
        />
      ];
    }

    return [
      // eslint-disable-next-line react/jsx-key
      <GridActionsCellItem
        icon={<EditIcon/>}
        label="Edit"
        className="textPrimary"
        onClick={handleEditClick(rowId)}
        color="inherit"
      />,
      // eslint-disable-next-line react/jsx-key
      <GridActionsCellItem
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
    setRowModesModel({...rowModesModel, [id]: {mode: GridRowModes.View}});
  };

  const handleDeleteClick = (id) => () => {
    setRows(rows.filter((row) => row.id !== id));
  };

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: {mode: GridRowModes.View, ignoreModifications: true}
    });

    const editedRow = rows.find((row) => row.id === id);
    if (editedRow.isNew) {
      setRows(rows.filter((row) => row.id !== id));
    }
  };

  const processRowUpdate = (newRow) => {
    const updatedRow = {...newRow, isNew: false};
    setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const getDataColumns = () => {
    let mainColumns = getMainColumns();
    mainColumns.push({
      headerName: '',
      field: 'row_actions',
      type: 'actions',
      cellClassName: 'row-actions',
      flex: 0.3,
      getActions: ({id}) => {
        return getRowActions(id);
      }
    })
    return mainColumns.map((col) => {
      return col.field === 'identity' ? updateFilterAndSortPropertiesToColumn(col) : updateFilterAndSortPropertiesToColumn(col, false, false);
    });
  }

  return (
    <>
      <Accordion>
        <AccordionSummary
          expandIcon={<></>}
          aria-controls="new-credential-pairs-content"
          id="new-credential-pairs-panel"
        >
          <Typography>ADD NEW ROW</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            <XDataGrid columns={newRowColumns} rows={[]} showToolbar={false}/>
          </Typography>
        </AccordionDetails>
      </Accordion>

      <XDataGrid columns={getDataColumns()}
                 rows={rows}
                 rowHeight={'25px'}
                 showToolbar={false}
                 maxHeight={'400px'}
                 editMode="row"
                 rowModesModel={rowModesModel}
                 onRowModesModelChange={handleRowModesModelChange}
                 onRowEditStop={handleRowEditStop}
                 processRowUpdate={processRowUpdate}
      />
    </>
  );
}

export default CredentialPairs;
