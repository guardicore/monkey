import { styled } from '@mui/system';
import { Accept, useDropzone } from 'react-dropzone';
import { fileUploadStyle, StyleProps } from '@/_components/file-upload/style';
import { ReactNode } from 'react';

export enum UploadStatus {
    ACCEPTED = 'ACCEPTED',
    REJECTED = 'REJECTED',
    IDLE = 'IDLE'
}

const UploadContainer = styled('div')<StyleProps>(fileUploadStyle as any);

type MonkeyFileUploadProps = {
    onDrop: (acceptedFiles: any, rejectedFiles: any) => void;
    maxFiles: number;
    accept: Accept;
    children: ReactNode;
    uploadStatus: UploadStatus;
    disabled?: boolean;
};

const MonkeyFileUpload = (props: MonkeyFileUploadProps) => {
    const { onDrop, maxFiles, accept, uploadStatus, disabled = false } = props;

    const { getRootProps, getInputProps } = useDropzone({
        onDrop: onDrop,
        maxFiles: maxFiles,
        accept: accept
    });

    return (
        <UploadContainer
            {...getRootProps()}
            uploadStatus={uploadStatus}
            disabled={disabled}>
            <input {...getInputProps()} />
            {props.children}
        </UploadContainer>
    );
};

export default MonkeyFileUpload;
