import MenuItem from '@mui/material/MenuItem';

// eslint-disable-next-line react/display-name
export const buildAvatarMenu = (LogoutButton) => () => {
    return (
        <MenuItem>
            <LogoutButton />
        </MenuItem>
    );
};

export default buildAvatarMenu;
