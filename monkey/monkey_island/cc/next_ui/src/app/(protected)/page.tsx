import classes from './page.module.scss';
import GettingStarted from '@/_components/getting-started/GettingStarted';

export default function AppHome() {
    return (
        <div id={classes['app-root-page']}>
            <GettingStarted />
        </div>
    );
}
