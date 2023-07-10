import React from 'react';
import AuthService from '../services/AuthService';

class AuthComponent extends React.Component {
    constructor(props) {
        super(props);
        this.auth = new AuthService();
        this.authFetch = this.auth.authFetch;
    }
}

export default AuthComponent;
