import LoadingScreen from '../ui-components/LoadingScreen';
import React, {useState} from 'react';
import AuthService from '../../services/AuthService';
import {Redirect} from 'react-router-dom';

const LogoutPage = (props) => {
  const [logoutDone, setLogoutDone] = useState(false);
  const auth = new AuthService();

  auth.logout()
    .then(res => {
      if(res.meta.code === 200){
        setLogoutDone(true);
        props.onStatusChange();
      }
    })

  if (logoutDone) {
    return <Redirect to={'/'} />
  } else {
    return <LoadingScreen text={"Logging out"} />
  }
}
export default LogoutPage;
