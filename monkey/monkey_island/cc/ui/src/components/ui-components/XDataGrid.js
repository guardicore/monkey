import React, {useEffect, useState} from 'react';
import {DataGrid, gridFilteredTopLevelRowCountSelector, GridToolbar, GridToolbarContainer} from '@mui/x-data-grid';
import CustomNoRowsOverlay from './utils/GridNoRowsOverlay';
import _ from 'lodash';
import '../../styles/components/XDataGrid.scss';

const DEFAULT_PAGE_SIZE = 10;
const PAGE_SIZE_OPTIONS = [10, 25, 50, 100];
const DEFAULT_MIN_WIDTH = '150px';
const FLEX = 'flex';
const MIN_WIDTH = 'minWidth';
const TOOLBAR = 'toolbar';
const HIDDEN = 'hidden';
const HIDE_TOOLBAR_ACTIONS = 'toolbar-actions-hidden'


const gridInitialState = {
  pagination: {paginationModel: {pageSize: DEFAULT_PAGE_SIZE}}
};

const prepareColsWidth = (columns) => {
  let updatedColumns = _.cloneDeep(columns);
  updatedColumns?.forEach((col) => {
    if (!(FLEX in col)) {
      col[FLEX] = 0.5;
    }
    if (!(MIN_WIDTH in col)) {
      col[MIN_WIDTH] = DEFAULT_MIN_WIDTH;
    }
  });

  return updatedColumns;
}

const prepareSlots = (toolbar, showToolbar) => {
  let slotsObj = {
    noRowsOverlay: CustomNoRowsOverlay,
    noResultsOverlay: CustomNoRowsOverlay
  };

  if (showToolbar) {
    slotsObj[TOOLBAR] = toolbar || GridToolbar;
  }

  return slotsObj;
}

const XDataGrid = (props) => {
  const {
    columns = [],
    rows = [],
    initialState = _.cloneDeep(gridInitialState),
    toolbar,
    density = X_DATA_GRID_DENSITY.STANDARD,
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
  const [hidePagination, setHidePagination] = useState(false);
  const [isDataEmpty, setIsDataEmpty] = useState(false);

  useEffect(() => {
    setUpdatedColumns(prepareColsWidth(columns));
    setSlots(prepareSlots(toolbar, showToolbar));
    prepareInitialState();
    setHidePagination(rows?.length <= DEFAULT_PAGE_SIZE);
    setIsDataEmpty(rows?.length === 0)
  }, []);

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
        pageSizeOptions={PAGE_SIZE_OPTIONS}
        getRowHeight={() => 'auto'}
        density={density}
        slots={slots}
        disableRowSelectionOnClick
        disableColumnFilter={disableColumnFilter}
        disableDensitySelector={disableDensitySelector}
        disableColumnMenu={disableColumnMenu}
        hideFooter={isDataEmpty}
        hideFooterPagination={hidePagination}
        classes={{columnHeaders: isDataEmpty ? HIDDEN : '', toolbarContainer: isDataEmpty ? HIDE_TOOLBAR_ACTIONS : ''}}
        {...rest}
      />
    </div>
  );
}

export default XDataGrid;

export const X_DATA_GRID_DENSITY = {
  COMPACT: 'compact',
  STANDARD: 'standard',
  COMFORTABLE: 'comfortable'
}

export const XDataGridTitle = ({title, showDataActionsToolbar = false}) => {
  return (
    <GridToolbarContainer>
      <div className="x-data-grid-title-wrapper">
        {title && <div className="x-data-grid-title">{title}</div>}
        {
          showDataActionsToolbar && <div className="x-grid-actions-toolbar-wrapper">
            <GridToolbar/>
          </div>
        }
      </div>
    </GridToolbarContainer>
  );
}
