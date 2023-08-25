import React, {useCallback, useLayoutEffect, useState} from 'react';
import {InputBase} from '@mui/material';
import {useGridApiContext} from '@mui/x-data-grid';

export const CREDENTIALS_ROW_KEYS = ['identity', 'password', 'lm', 'ntlm', 'ssh_public_key', 'ssh_private_key'];
export const IDENTITY_KEY = 'identity';
export const COLUMN_WIDTH = 166.5;

const HIDDEN_PASSWORD_STRING = '*****';

const multilineColumn = {
  type: 'string',
  renderEditCell: (params) => <EditTextarea {...params} />
};

const valueFormatter = (showSecrets = false) => {
  return {
    valueFormatter: (params) => {
      if (!params.value || showSecrets) {
        return params.value;
      }
      return HIDDEN_PASSWORD_STRING;
    }
  }
}
const EditTextarea = (props) => {
  const {id, field, value, hasFocus, error} = props;
  const [valueState, setValueState] = useState(value);
  const [inputRef, setInputRef] = useState(null);
  const apiRef = useGridApiContext();

  useLayoutEffect(() => {
    if (hasFocus && inputRef) {
      inputRef.focus();
    }
  }, [hasFocus, inputRef]);

  const handleChange = useCallback(
    (event) => {
      const newValue = event.target.value;
      setValueState(newValue);
      apiRef.current.setEditCellValue(
        {id, field, value: newValue, debounceMs: 200},
        event
      );
    },
    [apiRef, field, id]
  );

  const keyPress = (e) => {
    if (e.keyCode === 13) {
      e.preventDefault();
    }
  }

  return (
    <div style={{position: 'relative', alignSelf: 'flex-start'}} className={error ? 'Mui-error' : 'valid'}>
      <InputBase
        onKeyDown={keyPress}
        multiline
        rows={1}
        value={valueState}
        sx={{textarea: {resize: 'none'}, width: '100%', height: '100%'}}
        onChange={handleChange}
        inputRef={(ref) => setInputRef(ref)}
      />
    </div>
  );
}

export const getMainColumns = (setErrorForRow, showSecrets) => {
  return [
    {headerName: 'Identity', field: 'identity', editable: true},
    {headerName: 'Password', field: 'password', editable: true, ...valueFormatter(showSecrets)},
    {headerName: 'LM', field: 'lm', editable: true, ...valueFormatter(showSecrets)},
    {headerName: 'NTLM', field: 'ntlm', editable: true, ...valueFormatter(showSecrets)},
    {headerName: 'SSH Public key', field: 'ssh_public_key', editable: true, ...multilineColumn, ...valueFormatter(showSecrets)},
    {headerName: 'SSH Private key', field: 'ssh_private_key', editable: true, ...multilineColumn, ...valueFormatter(showSecrets),
    preProcessEditCellProps: (params) => {
        const isSSHPublicKeyProps = params.otherFieldsProps.ssh_public_key;
        const hasError = isSSHPublicKeyProps.value && !params.props.value;
        if (setErrorForRow) {
          hasError ? setErrorForRow(params.id, true) : setErrorForRow(params.id, false);
        }
        return {...params.props, error: hasError};
      }
    }
  ];
};

export const updateFilterAndSortPropertiesToColumn = (col, filterable = true, sortable = true) => {
  const colObj = {...col};
  colObj['filterable'] = filterable;
  colObj['sortable'] = sortable;
  return colObj;
};

export const getDataColumns = (getRowActions, disableAllColumnsFilterAndSort, setErrorForRow, rowActionsHeaderComponent, showSecrets = false) => {
  let mainColumns = getMainColumns(setErrorForRow, showSecrets);

  if(typeof getRowActions === 'function'){
    mainColumns.push({
      headerName: '',
      field: 'row_actions',
      type: 'actions',
      minWidth: 100,
      flexValue: 0.5,
      headerClassName: `row-actions--header`,
      cellClassName: `row-actions`,
      renderHeader: () => rowActionsHeaderComponent,
      getActions: ({id}) => {
        return getRowActions(id);
      }
    })
  }

  return mainColumns.map((col) => {
    if (disableAllColumnsFilterAndSort) {
      return updateFilterAndSortPropertiesToColumn(col, false, false);
    } else {
      return col.field === 'identity' ? updateFilterAndSortPropertiesToColumn(col) : updateFilterAndSortPropertiesToColumn(col, false, false);
    }
  });
}

export const isRowDuplicated = (newRow, existingRow) => {
  for (const key of CREDENTIALS_ROW_KEYS) {
    if (newRow?.[key] !== existingRow?.[key]) {
      return false;
    }
  }

  return true;
}

export const isAllValuesInRowAreEmpty = (row, keysToIgnore = [], isRowAnEditMode = false) => {
  if (row) {
    for (const key of CREDENTIALS_ROW_KEYS) {
      const value = isRowAnEditMode ? row?.[key]?.value : row?.[key];
      if (!keysToIgnore.includes(key) && value !== '' && value !== undefined) {
        return false;
      }
    }
  }
  return true;
}

export const setErrorsForRow = (prevState, rowId, isAddingError) => {
  const rowIdIndex = prevState?.indexOf(rowId);
  if (isAddingError && rowIdIndex === -1) {
    return [...prevState, rowId];
  } else if (!isAddingError && rowIdIndex >= 0) {
    let copyOfPrevSate = [...prevState];
    copyOfPrevSate.splice(rowIdIndex, 1);
    return copyOfPrevSate;
  }
  return prevState;
}

export const trimRowValues = (row) => {
  const rowCopy = {...row};
  CREDENTIALS_ROW_KEYS.forEach(key => {
    if(rowCopy[key] !== undefined) {
      rowCopy[key] = rowCopy[key].trim();
    } else {
      rowCopy[key] = '';
    }
  })
  return rowCopy;
}
