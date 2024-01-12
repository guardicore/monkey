import { store } from '@/redux/store';
import { Actions } from '@/redux/features/actions';

export const logout = () => store.dispatch({ type: Actions.LOGOUT });
