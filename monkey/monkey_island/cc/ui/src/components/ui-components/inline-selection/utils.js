export const COLUMN_SIZES = {
    LARGE: 'large',
    STANDARD: 'standard',
    SMALL: 'small'
};

export function getColumnSize(size) {
    if (size === undefined || size === COLUMN_SIZES.STANDARD) {
        return { lg: 9, md: 10, sm: 12 };
    } else if (size === COLUMN_SIZES.LARGE) {
        return { lg: 12, md: 12, sm: 12 };
    } else if (size === COLUMN_SIZES.SMALL) {
        return { lg: 7, md: 7, sm: 7 };
    }
}
