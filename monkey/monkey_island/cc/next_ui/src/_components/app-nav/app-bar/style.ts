export const appBarHeight = '64px';
export const appBar = {
    display: 'flex'
};

export const muiContainerRoot = {
    width: '100%',
    maxWidth: '100% !important',
    height: '100%'
};

export const muiToolbarRoot = {
    minHeight: appBarHeight,
    height: appBarHeight,
    display: 'flex',
    justifyContent: 'space-between'
};

export const logoAndMenuContainer = {
    display: 'flex',
    gap: '1rem',
    alignItems: 'center',
    width: '100%',
    height: '100%'
};

export const logoAndDrawerContainer = {
    display: 'flex',
    gap: '0',
    alignItems: 'center'
};

export const logoWrapper = {
    fontSize: '2.5rem',
    '&:hover': {
        cursor: 'pointer'
    }
};

export const etcContainer = {
    display: 'flex',
    gap: '1rem',
    alignItems: 'center',
    '& .profile-avatar': {
        fontSize: '2.5rem'
    }
};

export const appRouterLink = {
    height: appBarHeight
};
