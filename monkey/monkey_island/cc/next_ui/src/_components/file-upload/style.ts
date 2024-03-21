import { UploadStatus } from '@/_components/file-upload/MonkeyFileUpload';
import { Theme } from '@mui/system';

export interface StyleProps {
    theme: Theme;
    uploadStatus: UploadStatus;
    disabled: boolean;
}
export const fileUploadStyle = ({
    theme,
    uploadStatus,
    disabled
}: StyleProps) => {
    const getColor = () => {
        if (disabled) {
            return theme.palette.action.disabled;
        } else if (uploadStatus == UploadStatus.ACCEPTED) {
            return theme.palette.success.main;
        } else if (uploadStatus == UploadStatus.REJECTED) {
            return theme.palette.error.main;
        }
        return theme.palette.primary.main;
    };

    return {
        color: getColor(),
        borderColor: getColor(),
        cursor: disabled ? 'default' : 'pointer',
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        borderWidth: '2px',
        borderRadius: '2px',
        borderStyle: 'dashed',
        outline: 'none',
        transition: 'border 0.24s ease-in-out'
    };
};
