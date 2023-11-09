import styles from './page.module.css';
import Test from '@/_components/Test';
// import { ThemeMode } from '@/_components/theme-mode/ThemeMode';

export default function Home() {
    return (
        <main className={styles.main}>
            <Test />
        </main>
    );
}
