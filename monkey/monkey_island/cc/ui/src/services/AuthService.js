import {SHA3} from 'sha3';
import decode from 'jwt-decode';

export default class AuthService {
  NO_AUTH_CREDS = '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()';

  SECONDS_BEFORE_JWT_EXPIRES = 20;
  AUTHENTICATION_API_ENDPOINT = '/api/auth';
  REGISTRATION_API_ENDPOINT = '/api/registration';

  login = (username, password) => {
    return this._login(username, password);
  };

  authFetch = (url, options) => {
    return this._authFetch(url, options);
  };

  jwtHeader = () => {
    if (this._loggedIn()) {
      return 'Bearer ' + this._getToken();
    }
  };

  _login = (username, password) => {
    return this._authFetch(this.AUTHENTICATION_API_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        username,
        password
      })
    }).then(response => response.json())
      .then(res => {
        if (Object.prototype.hasOwnProperty.call(res, 'access_token')) {
          this._setToken(res['access_token']);
          return {result: true};
        } else {
          this._removeToken();
          return {result: false};
        }
      })
  };

  register = (username, password) => {
    if (password !== '') {
      return this._register(username, password);
    } else {
      return this._register(username, password);
    }
  };

  _register = (username, password) => {
    return this._authFetch(this.REGISTRATION_API_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        'user': username,
        'password': password
      })
    }).then(res => {
      if (res.status === 200) {
        return this._login(username, password)
      } else {
        return res.json().then(res_json => {
          return {result: false, error: res_json['error']};
        })
      }
    })
  };

  _authFetch = (url, options = {}) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this._loggedIn()) {
      headers['Authorization'] = 'Bearer ' + this._getToken();
    }

    if (Object.prototype.hasOwnProperty.call(options, 'headers')) {
      for (let header in headers) {
        options['headers'][header] = headers[header];
      }
    } else {
      options['headers'] = headers;
    }

    return fetch(url, options)
      .then(res => {
        if (res.status === 401) {
          res.clone().json().then(res_json => {
            console.log('Got 401 from server while trying to authFetch: ' + JSON.stringify(res_json));
          });
          this._removeToken();
        }
        return res;
      })
  };

  needsRegistration = () => {
    return fetch(this.REGISTRATION_API_ENDPOINT,
      {method: 'GET'})
      .then(response => response.json())
      .then(res => {
        return res['needs_registration']
      })
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
      return decode(token)['exp'] - this.SECONDS_BEFORE_JWT_EXPIRES < Date.now() / 1000;
    } catch (err) {
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

}
