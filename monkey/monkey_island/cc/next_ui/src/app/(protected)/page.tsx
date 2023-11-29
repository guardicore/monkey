import styles from './page.module.scss';
import Test from '@/_components/Test';

export default function Home() {
    return (
        // <Test />
        // <main className={styles.main}>
        <div className={styles.test}>
            <Test />
        </div>
        // </main>
    );
}
