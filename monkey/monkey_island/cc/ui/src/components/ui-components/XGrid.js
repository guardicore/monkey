import React, {useEffect, useState} from 'react';
import {DataGrid, gridFilteredTopLevelRowCountSelector, GridToolbar, GridToolbarContainer} from '@mui/x-data-grid';
import CustomNoRowsOverlay from './utils/GridNoRowsOverlay';
import _ from 'lodash';
import '../../styles/components/XGrid.scss';

const DEFAULT_PAGE_SIZE = 10;
const DEFAULT_MIN_WIDTH = '150px';
const FLEX = 'flex';
const MIN_WIDTH = 'minWidth';
const TOOLBAR = 'toolbar';

export const XGridTitle = ({title, showDataActionsToolbar = false}) => {
  return (
    <GridToolbarContainer>
      <div className="x-data-grid-title-wrapper">
        <div className="x-data-grid-title">{title}</div>
        {
          showDataActionsToolbar && <div className="x-grid-actions-toolbar-wrapper">
            <GridToolbar />
          </div>
        }
      </div>
    </GridToolbarContainer>
  );
}

const gridInitialState = {
  pagination: {paginationModel: {pageSize: DEFAULT_PAGE_SIZE}}
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
    disableColumnMenu = true,
    height,
    ...rest
  } = {...props}

  const [updatedColumns, setUpdatedColumns] = useState(columns);
  const [updatedInitialState, setUpdatedInitialState] = useState(initialState)
  const [slots, setSlots] = useState({});
  const [gridVisibleFilteredRowsCount, setGridVisibleFilteredRowsCount] = useState(0);
  const [hideFooter, setHideFooter] = useState(false);

  useEffect(() => {
    console.log(toolbar);
    handleColsWidth();
    prepareSlots();
    prepareInitialState();
    setHideFooter(rows?.length === 0 || rows?.length <= DEFAULT_PAGE_SIZE);
  }, []);

  const handleColsWidth = () => {
    let columnsToUpdate = _.cloneDeep(columns);
    columnsToUpdate?.forEach((col) => {
      if (!(FLEX in col)) {
        col[FLEX] = 0.5;
      }
      if (!(MIN_WIDTH in col)) {
        col[MIN_WIDTH] = DEFAULT_MIN_WIDTH;
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
      slotsObj[TOOLBAR] = toolbar
    }

    setSlots(slotsObj);
  }

  const prepareInitialState = () => {
    setUpdatedInitialState(Object.assign(_.cloneDeep(gridInitialState), initialState));
  }

  const handleGridState = (state) => {
    const visibleFilteredRowsCount = state ? (gridFilteredTopLevelRowCountSelector(state) || 0) : 0;
    setGridVisibleFilteredRowsCount(visibleFilteredRowsCount);
  }

  return (
    <div className="x-data-grid"
         style={{height: `${!rows?.length || !gridVisibleFilteredRowsCount ? '300px' : (height || 'auto')}`}}>
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
        hideFooter={hideFooter}
        hideFooterPagination={hideFooter}
        {...rest}
      />
    </div>
  );
}

export default XGrid;
