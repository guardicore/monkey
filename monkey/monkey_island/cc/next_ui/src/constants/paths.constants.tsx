import HomeIcon from '@mui/icons-material/Home';
import EventNoteIcon from '@mui/icons-material/EventNote';
import HubIcon from '@mui/icons-material/Hub';

export enum AUTH_PATHS {
    SIGN_IN = '/signin',
    SIGN_UP = '/signup'
}

export const AUTHENTICATED_ROOT_PATH = '/';

export const AUTHENTICATED_PATHS = [
    { path: '/home', label: 'Home', icon: <HomeIcon /> },
    { path: '/map', label: 'Map', icon: <HubIcon /> },
    { path: '/events', label: 'Events', icon: <EventNoteIcon /> }
];
