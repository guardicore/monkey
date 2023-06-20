import React, {useEffect, useState} from 'react';
import {DataGrid, gridFilteredTopLevelRowCountSelector, GridToolbar} from '@mui/x-data-grid';
import CustomNoRowsOverlay from './utils/GridNoRowsOverlay';
import _ from 'lodash';
import '../../styles/components/XGrid.scss';

export const XGridTitle = ({title, showToolbar = false}) => {
  return (
    <div className="x-data-grid-title-wrapper">
      <div className="x-data-grid-title">{title}</div>
      {
        showToolbar && <div className="x-grid-toolbar-wrapper">
          <GridToolbar/>
        </div>
      }
    </div>
  );
}

const gridInitialState = {
  pagination: {paginationModel: {pageSize: 10}}
};

const XGrid = (props) => {
  const {
    columns = [],
    rows = [],
    initialState = _.cloneDeep(gridInitialState),
    toolbar = GridToolbar,
    showToolbar = true,
    disableColumnFilter = false,
    disableDensitySelector = true,
    disableColumnMenu = true
  } = {...props}

  const [updatedColumns, setUpdatedColumns] = useState(columns);
  const [updatedInitialState, setUpdatedInitialState] = useState(initialState)
  const [slots, setSlots] = useState({});
  const [gridVisibleFilteredRowsCount, setGridVisibleFilteredRowsCount] = useState(0);

  useEffect(() => {
    handleColsWidth();
    prepareSlots();
    prepareInitialState();
  }, []);

  const handleColsWidth = () => {
    let columnsToUpdate = _.cloneDeep(columns);
    columnsToUpdate?.forEach((col) => {
      if (!('flex' in col)) {
        col['flex'] = 0.5;
      }
      if (!('minWidth' in col)) {
        col['minWidth'] = '150px'
      }
    });

    setUpdatedColumns(columnsToUpdate);
  }

  const prepareSlots = () => {
    let slotsObj = {
      noRowsOverlay: CustomNoRowsOverlay,
      noResultsOverlay: CustomNoRowsOverlay
    };

    if (showToolbar) {
      slotsObj['toolbar'] = toolbar
    }

    setSlots(slotsObj);
  }

  const prepareInitialState = () => {
    setUpdatedInitialState(Object.assign(_.cloneDeep(gridInitialState), initialState));
  }

  const handleGridState = (state) => {
    console.log(state);
    const visibleFilteredRowsCount = state ? (gridFilteredTopLevelRowCountSelector(state) || 0) : 0;
    setGridVisibleFilteredRowsCount(visibleFilteredRowsCount);
  }

  return (
    <div className="x-data-grid"
         style={{height: `${!rows?.length || !gridVisibleFilteredRowsCount ? '300px' : 'auto'}`}}>
      <DataGrid
        onStateChange={handleGridState}
        columns={updatedColumns}
        rows={[...rows]}
        initialState={{...updatedInitialState}}
        pageSizeOptions={[10, 25, 50, 100]}
        getRowHeight={() => 'auto'}
        slots={slots}
        disableRowSelectionOnClick
        disableColumnFilter={disableColumnFilter}
        disableDensitySelector={disableDensitySelector}
        disableColumnMenu={disableColumnMenu}
      />
    </div>
  );
}

export default XGrid;
