import React, { useEffect, useMemo, useState } from 'react';
import {
    DataGrid,
    gridFilteredTopLevelRowCountSelector,
    GridToolbar,
    GridToolbarContainer
} from '@mui/x-data-grid';
import _ from 'lodash';
import CustomNoRowsOverlay from '@/app/(protected)/plugins/_lib/no-rows-overlay/GridNoRowsOverlay';
import MonkeyTooltip from '@/_components/tooltips/MonkeyTooltip';

const X_DATA_GRID_CLASS = 'x-data-grid';
const DEFAULT_PAGE_SIZE = 10;
const PAGE_SIZE_OPTIONS = [10, 25, 50, 100];
const DEFAULT_MIN_WIDTH = 150;
const DEFAULT_MAX_WIDTH = DEFAULT_MIN_WIDTH;
const IS_TEXTUAL = 'isTextual';
const RENDER_CELL = 'renderCell';
const WIDTH = 'width';
const MIN_WIDTH = 'minWidth';
const MAX_WIDTH = 'maxWidth';
const TOOLBAR = 'toolbar';
const HIDDEN = 'hidden';
const HIDE_TOOLBAR_ACTIONS = 'toolbar-actions-hidden';
const HEADER_CLASS_NAME = 'headerClassName';
const CELL_CLASS_NAME = 'cellClassName';
const COLUMN_WIDTH = { min: DEFAULT_MIN_WIDTH, max: DEFAULT_MAX_WIDTH };
const FLEX_VALUES = {
    0: 'flex-0',
    0.5: 'flex-0.5',
    1: 'flex-1'
};

const gridInitialState = {
    pagination: { paginationModel: { pageSize: DEFAULT_PAGE_SIZE } }
};

const setColumnClass = (column, classToAppend) => {
    column[HEADER_CLASS_NAME] = column[HEADER_CLASS_NAME]
        ? `${column[HEADER_CLASS_NAME]} ${classToAppend}`
        : classToAppend;
    column[CELL_CLASS_NAME] = column[CELL_CLASS_NAME]
        ? `${column[CELL_CLASS_NAME]} ${classToAppend}`
        : classToAppend;
};

const prepareColsClasses = (columns, setFlex) => {
    const updatedColumns = _.cloneDeep(columns) || [];
    updatedColumns?.forEach((col) => {
        if (col[MAX_WIDTH] === Infinity) {
            setColumnClass(col, X_DATA_GRID_CLASSES.MAX_WIDTH_NONE);
        }

        if (setFlex) {
            if (col?.flexValue >= 0) {
                setColumnClass(
                    col,
                    FLEX_VALUES[col.flexValue] || FLEX_VALUES[1]
                );
            } else {
                setColumnClass(col, FLEX_VALUES[1]);
            }
        }
    });

    return updatedColumns;
};

const prepareColsWidth = (columns, columnWidth, setColWidth) => {
    const colWidth = getColumnWidth(columnWidth);
    const updatedColumns = _.cloneDeep(columns) || [];
    if (setColWidth) {
        updatedColumns?.forEach((col) => {
            if (!(WIDTH in col)) {
                if (!(MIN_WIDTH in col)) {
                    col[MIN_WIDTH] = colWidth?.min || DEFAULT_MIN_WIDTH;
                }
                if (!(MAX_WIDTH in col) && colWidth?.max >= 0) {
                    col[MAX_WIDTH] = colWidth?.max || DEFAULT_MAX_WIDTH;
                } else {
                    col[MAX_WIDTH] = Infinity;
                }
            }
        });
    }
    return updatedColumns;
};

const prepareColsCustomTooltip = (columns) => {
    const updatedColumns = _.cloneDeep(columns) || [];
    updatedColumns?.forEach((col) => {
        if (col[IS_TEXTUAL]) {
            // eslint-disable-next-line react/display-name
            col[RENDER_CELL] = (params) =>
                params?.value ? (
                    <MonkeyTooltip
                        isOverflow={true}
                        title={params?.value?.toString()}>
                        {params?.value?.toString()}
                    </MonkeyTooltip>
                ) : undefined;
        }
    });
    return updatedColumns;
};

const prepareSlots = (toolbar, showToolbar) => {
    const slotsObj = {
        noRowsOverlay: CustomNoRowsOverlay,
        noResultsOverlay: CustomNoRowsOverlay,
        baseTooltip: MonkeyTooltip
    };

    if (showToolbar) {
        slotsObj[TOOLBAR] = toolbar || GridToolbar;
    }

    return slotsObj;
};

const getColumnWidth = (columnWidth) => {
    const colWidth = { ...COLUMN_WIDTH, ...columnWidth };
    if (colWidth?.max < colWidth?.min && colWidth?.max >= 0) {
        colWidth.max = colWidth.min;
    } else if (colWidth?.min > colWidth?.max && colWidth?.max >= 0) {
        colWidth.min = colWidth.max;
    }

    return colWidth;
};

const MonkeyDataGrid = (props) => {
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
        hideHeaders = false,
        setColWidth = true,
        setFlex = true,
        sortingOrder = ['asc', 'desc'],
        height,
        maxHeight,
        rowHeight,
        columnWidth,
        className,
        needCustomWorkaround = true,
        noRowsOverlayMessage,
        ...rest
    } = { ...props };

    const [updatedInitialState, setUpdatedInitialState] =
        useState(initialState);
    const [slots, setSlots] = useState({});
    const [gridVisibleFilteredRowsCount, setGridVisibleFilteredRowsCount] =
        useState(0);
    const [hidePagination, setHidePagination] = useState(false);
    const [isDataEmpty, setIsDataEmpty] = useState(false);

    const gridWrapperClassName = className
        ? `${X_DATA_GRID_CLASS} ${className}`
        : X_DATA_GRID_CLASS;
    const sx = { maxHeight: maxHeight || height || 'auto' };

    const updatedColumns = useMemo(() => {
        const mutatedColumns = prepareColsCustomTooltip(columns);
        return needCustomWorkaround
            ? prepareColsClasses(
                  prepareColsWidth(mutatedColumns, columnWidth, setColWidth),
                  setFlex
              )
            : mutatedColumns;
    }, [columns]);

    useEffect(() => {
        setSlots(prepareSlots(toolbar, showToolbar));
        prepareInitialState();
    }, []);

    useEffect(() => {
        setHidePagination(rows?.length <= DEFAULT_PAGE_SIZE);
        setIsDataEmpty(rows?.length === 0);
    }, [rows?.length]);

    const prepareInitialState = () => {
        setUpdatedInitialState(
            Object.assign(_.cloneDeep(gridInitialState), initialState)
        );
    };

    const handleGridState = (state) => {
        const visibleFilteredRowsCount = state
            ? gridFilteredTopLevelRowCountSelector(state) || 0
            : 0;
        setGridVisibleFilteredRowsCount(visibleFilteredRowsCount);
    };

    return (
        <div
            className={gridWrapperClassName}
            style={{
                height: `${
                    !rows?.length || !gridVisibleFilteredRowsCount
                        ? '300px'
                        : height || 'auto'
                }`
            }}>
            <DataGrid
                onStateChange={handleGridState}
                columns={updatedColumns}
                rows={[...rows]}
                initialState={{ ...updatedInitialState }}
                pageSizeOptions={PAGE_SIZE_OPTIONS}
                getRowHeight={() => rowHeight || 'auto'}
                density={density}
                slots={slots}
                sortingOrder={sortingOrder}
                disableRowSelectionOnClick
                disableColumnFilter={disableColumnFilter}
                disableDensitySelector={disableDensitySelector}
                disableColumnMenu={disableColumnMenu}
                hideFooter={hidePagination}
                hideFooterPagination={hidePagination}
                classes={{
                    columnHeaders: isDataEmpty || hideHeaders ? HIDDEN : '',
                    toolbarContainer: isDataEmpty ? HIDE_TOOLBAR_ACTIONS : ''
                }}
                slotProps={{
                    toolbar: { printOptions: { disableToolbarButton: true } },
                    noRowsOverlay: { message: noRowsOverlayMessage }
                }}
                sx={sx}
                {...rest}
            />
        </div>
    );
};

export default MonkeyDataGrid;

export const X_DATA_GRID_DENSITY = {
    COMPACT: 'compact',
    STANDARD: 'standard',
    COMFORTABLE: 'comfortable'
};

export const X_DATA_GRID_CLASSES = {
    MAX_WIDTH_NONE: 'max-width-none',
    HIDDEN_LAST_EMPTY_CELL: 'last-empty-cell-hidden'
};

export const XDataGridTitle = ({ title, showDataActionsToolbar = false }) => {
    return (
        <GridToolbarContainer>
            <div className="x-data-grid-title-wrapper">
                {title && <div className="x-data-grid-title">{title}</div>}
                {showDataActionsToolbar && (
                    <div className="x-grid-actions-toolbar-wrapper">
                        <GridToolbar />
                    </div>
                )}
            </div>
        </GridToolbarContainer>
    );
};
