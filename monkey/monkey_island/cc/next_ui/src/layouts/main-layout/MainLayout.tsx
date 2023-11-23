import classes from './mainLayout.module.scss';
// import MonkeyAppBar from '@/_components/app-bar/AppBar';

export default function MainLayout({
    children
}: {
    children: React.ReactNode;
}) {
    return (
        <div id={classes['main-layout']}>
            <div id="app-bar-wrapper">app bar for monkey</div>
            <main id="app-content-wrapper">{children}</main>
        </div>
    );
}
