import { clearTimer } from '@/redux/features/api/authentication/authenticationTimerSlice';
import { store } from '@/redux/store';
import _ from 'lodash';

const clearAuthenticationTimer = () => {
    const storedTimer = _.cloneDeep(store.getState().authenticationTimer.timer);
    if (storedTimer !== null) {
        clearTimeout(storedTimer);
    }
    store.dispatch(clearTimer());
};

export default clearAuthenticationTimer;
