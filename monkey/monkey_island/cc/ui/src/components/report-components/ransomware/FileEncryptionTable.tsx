import React from 'react';
import XDataGrid, { XDataGridTitle } from '../../ui-components/XDataGrid';

type TableRow = {
    hostname: string;
    file_path: number;
    id: any;
    encryption_algorithm: string;
};

const customToolbar = () => {
    return <XDataGridTitle title={'Encrypted Files'} showDataActionsToolbar={false} />;
};

const columns = [
    { headerName: 'Host', field: 'hostname' },
    { headerName: 'File Path', field: 'file_path', flex: 0.8 },
    { headerName: 'Encryption Algorithm', field: 'encryption_algorithm' }
];

const FileEncryptionTable = ({ tableData }: { tableData: Array<TableRow> }) => {
    return (
        <>
            <h3 className={'report-section-header'}>File encryption</h3>

            <XDataGrid
                toolbar={customToolbar}
                columns={columns}
                rows={[...tableData]}
                maxHeight={'300px'}
            />
        </>
    );
};

export { FileEncryptionTable, TableRow };
