export const mainLayout = {
    height: '100vh',
    width: '100vw',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column'
};

export const appContentWrapper = {
    flex: 1,
    display: 'flex',
    overflow: 'hidden',
    '& > *': {
        width: '100%'
    }
};
