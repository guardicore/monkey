export default class AuthService {
  LOGIN_ENDPOINT = '/api/login';
  LOGOUT_ENDPOINT = '/api/logout';
  REGISTRATION_API_ENDPOINT = '/api/register';
  REGISTRATION_STATUS_API_ENDPOINT = '/api/registration-status';

  login = (username, password) => {
    return this._login(username, password);
  };

  logout = () => {
    return this._authFetch(this.LOGOUT_ENDPOINT);
  }

  authFetch = (url, options) => {
    return this._authFetch(url, options);
  };

  jwtHeader = () => {
    if (this.loggedIn()) {
      return 'Bearer ' + this._getToken();
    }
  };

  _login = (username, password) => {
    return this._authFetch(this.LOGIN_ENDPOINT, {
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
    return this._register(username, password);
  };

  _register = (username, password) => {
    return this._authFetch(this.REGISTRATION_API_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        'username': username,
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

    if (this.loggedIn()) {
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
    return fetch(this.REGISTRATION_STATUS_API_ENDPOINT,
      {method: 'GET'})
      .then(response => response.json())
      .then(res => {
        return res['needs_registration']
      })
  };

  loggedIn() {
    const token = this._getToken();
    return ((token !== null) && !this._isTokenExpired(token));
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
