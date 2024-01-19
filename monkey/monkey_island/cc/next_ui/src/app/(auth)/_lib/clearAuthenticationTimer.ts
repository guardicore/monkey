import { clearTimer } from '@/redux/features/api/authenticationTimerSlice';
import { store } from '@/redux/store';
import _ from 'lodash';

const clearAuthenticationTimer = () => {
    const storedTimer = _.cloneDeep(
        store.getState().authenticationTimeout.timer
    );
    if (storedTimer !== null) {
        clearTimeout(storedTimer);
    }
    store.dispatch(clearTimer());
};

export default clearAuthenticationTimer;
