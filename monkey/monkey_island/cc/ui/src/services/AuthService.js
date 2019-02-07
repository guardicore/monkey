import { SHA3 } from 'sha3';
import decode from 'jwt-decode';
import {SERVER_CONFIG} from '../server_config/ServerConfig';

export default class AuthService {
  AUTH_ENABLED = SERVER_CONFIG.isAuthEnabled();

  login = (username, password) => {
    if (this.AUTH_ENABLED) {
      return this._login(username, this.hashSha3(password));
    } else {
      return {result: true};
    }
  };

  authFetch = (url, options) => {
    if (this.AUTH_ENABLED) {
      return this._authFetch(url, options);
    } else {
      return fetch(url, options);
    }
  };

  hashSha3(text) {
    let hash = new SHA3(512);
    hash.update(text);
    return this._toHexStr(hash.digest());
  }

  _login = (username, password) => {
    return this._authFetch('/api/auth', {
      method: 'POST',
      body: JSON.stringify({
        username,
        password
      })
    }).then(response => response.json())
      .then(res => {
        if (res.hasOwnProperty('access_token')) {
          this._setToken(res['access_token']);
          return {result: true};
        } else {
          this._removeToken();
          return {result: false};
        }

      })
  };

  _authFetch = (url, options = {}) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this.loggedIn()) {
      headers['Authorization'] = 'JWT ' + this._getToken();
    }

    if (options.hasOwnProperty('headers')) {
      for (let header in headers) {
        options['headers'][header] = headers[header];
      }
    } else {
      options['headers'] = headers;
    }

    return fetch(url, options)
      .then(res => {
        if (res.status === 401) {
          this._removeToken();
        }
        return res;
      });
  };

  loggedIn() {
    if (!this.AUTH_ENABLED) {
      return true;
    }

    const token = this._getToken();
    return ((token !== null) && !this._isTokenExpired(token));
  }

  logout() {
    if (this.AUTH_ENABLED) {
      this._removeToken();
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

  _removeToken() {
    localStorage.removeItem('jwt');
  }

  _getToken() {
    return localStorage.getItem('jwt')
  }

  _toHexStr(byteArr) {
    return byteArr.reduce((acc, x) => (acc + ('0' + x.toString(0x10)).slice(-2)), '');
  }


}
