import decode from 'jwt-decode';

export default class AuthService {
  AUTH_ENABLED = true;

  login = (username, password) => {
    if (this.AUTH_ENABLED) {
      return this._login(username, password);
    } else {
      return {};
    }
  };

  authFetch = (url, options) => {
    if (this.AUTH_ENABLED) {
      return this._authFetch(url, options);
    } else {
      return fetch(url, options);
    }
  };

  _login = (username, password) => {
    return this._authFetch('/api/auth', {
      method: 'POST',
      body: JSON.stringify({
        username,
        password
      })
    }).then(response => response.json())
      .then(res => {
        this._setToken(res['access_token']);
      })
  };

  _authFetch = (url, options) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this.loggedIn()) {
      headers['Authorization'] = 'JWT ' + this._getToken();
    }

    return fetch(url, {
      headers,
      ...options
    });

  };

  loggedIn() {
    if (!this.AUTH_ENABLED) {
      return true;
    }
    const token = this._getToken();
    return (token && !this._isTokenExpired(token));
  }

  logout() {
    if (this.AUTH_ENABLED) {
      localStorage.removeItem('jwt');
    }
  }

  _isTokenExpired(token) {
    try {
      return decode(token)['exp'] < Date.now() / 1000;
    }
    catch (err) {
      return false;
    }
  }

  _setToken(idToken) {
    localStorage.setItem('jwt', idToken);
  }

  _getToken() {
    return localStorage.getItem('jwt')
  }


}
