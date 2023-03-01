import _ from 'lodash';

export default class AuthService {
  LOGIN_ENDPOINT = '/api/login?include_auth_token';
  LOGOUT_ENDPOINT = '/api/logout';
  REGISTRATION_API_ENDPOINT = '/api/register?include_auth_token';
  REGISTRATION_STATUS_API_ENDPOINT = '/api/registration-status';

  TOKEN_NAME_IN_LOCALSTORAGE = 'authentication_token';
  TOKEN_NAME_IN_RESPONSE = 'authentication_token';

  login = (username, password) => {
    return this._login(username, password);
  };

  logout = () => {
    return this._authFetch(this.LOGOUT_ENDPOINT, {method: 'POST'})
      .then(response => response.json())
      .then(response => {
        if(response.meta.code === 200){
          this._removeToken();
        }
        return response;
      });
  }

  authFetch = (url, options) => {
    return this._authFetch(url, options);
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
        let token = this._getTokenFromResponse(res);
        if (token !== undefined) {
          this._setToken(token);
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
          console.log(res_json);
          return {result: false, error: res_json['response']['errors']};
        })
      }
    })
  };

  _getTokenFromResponse= (response) => {
    return _.get(response, 'response.user.'+this.TOKEN_NAME_IN_RESPONSE, undefined);
  }

  _authFetch = (url, options = {}) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this.loggedIn()) {
      headers['Authentication-Token'] = this._getToken();
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
    return (token !== null);
  }

  _setToken(idToken) {
    localStorage.setItem(this.TOKEN_NAME_IN_LOCALSTORAGE, idToken);
  }

  _removeToken() {
    localStorage.removeItem(this.TOKEN_NAME_IN_LOCALSTORAGE);
  }

  _getToken() {
    return localStorage.getItem(this.TOKEN_NAME_IN_LOCALSTORAGE)
  }

}
