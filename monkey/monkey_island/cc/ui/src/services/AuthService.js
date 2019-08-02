import { SHA3 } from 'sha3';
import decode from 'jwt-decode';

export default class AuthService {
  // SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
  NO_AUTH_CREDS =
    "55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062" +
    "8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557";

  login = (username, password) => {
    return this._login(username, this.hashSha3(password));
  };

  authFetch = (url, options) => {
    return this._authFetch(url, options);
  };

  jwtHeader = () => {
    if (this._loggedIn()) {
      return 'JWT ' + this._getToken();
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

    if (this._loggedIn()) {
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

  async loggedIn() {
    let token = this._getToken();
    if ((token === null) || (this._isTokenExpired(token))) {
      await this.attemptNoAuthLogin();
    }
    return this._loggedIn();
  }

  attemptNoAuthLogin() {
    return this._login(this.NO_AUTH_CREDS, this.NO_AUTH_CREDS);
  }

  _loggedIn() {
    const token = this._getToken();
    return ((token !== null) && !this._isTokenExpired(token));
  }

  logout = () => {
    this._removeToken();
  };

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
