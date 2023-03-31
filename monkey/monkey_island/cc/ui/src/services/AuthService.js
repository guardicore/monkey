import React from 'react';

export function getErrors(errors) {
  const errorArray = [];

  for (let i=0; i<errors.length; i++) {
    const key = 'registration-error-' + i
    errorArray.push(<li key={key}>{errors[i]}</li>);
  }
  return <ul>{errorArray}</ul>;
}

export default class AuthService {
  LOGIN_ENDPOINT = '/api/login';
  LOGOUT_ENDPOINT = '/api/logout';
  REGISTRATION_API_ENDPOINT = '/api/register';
  REGISTRATION_STATUS_API_ENDPOINT = '/api/registration-status';

  REFRESH_AUTH_TOKEN_ENDPOINT = '/api/refresh-authentication-token'

  AUTH_TOKEN_NAME_IN_LOCALSTORAGE = 'authentication_token';
  AUTH_TOKEN_NAME_IN_RESPONSE = 'authentication_token';

  REFRESH_TOKEN_NAME_IN_LOCALSTORAGE = 'refresh_token';
  REFRESH_TOKEN_NAME_IN_RESPONSE = 'refresh_token';

  login = (username, password) => {
    return this._login(username, password);
  };

  logout = () => {
    return this._authFetch(this.LOGOUT_ENDPOINT, {method: 'POST'})
      .then(response => response.json())
      .then(response => {
        if(response.meta.code === 200){
          this._removeTokens(
            [this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE,
             this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE]
          );
        }
        return response;
      });
  }

  authFetch = (url, options) => {
    return this._authFetch(url, options).then(res => {
      if(res.status === 401){
        this._refreshAuthToken();
        return this._authFetch(url, options);
      }
      return res;
    });
  };

  _refreshAuthToken = () => {
    let refreshToken = this._getToken(this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE);
    if (refreshToken) {
      this._fetchNewTokenPair()
        .then(response => response.json().then(data => ({status: response.status, body: data})))
        .then(object => {
          if(object.status === 200) {
            this._setTokenPairFromResponseObject(object);
          } else if (object.status === 401) {
            this._removeTokens(
              [this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE,
               this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE]
            );
          }
        })
    }
  }

  _fetchNewTokenPair = () => {
    const options = {
      method: 'POST',
      // https://stackoverflow.com/questions/11508463/javascript-set-object-key-by-variable
      body: JSON.stringify({
        [this.REFRESH_TOKEN_NAME_IN_RESPONSE]: this._getToken(this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE)
      }),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }
    return fetch(this.REFRESH_AUTH_TOKEN_ENDPOINT, options);
  }

  _setTokenPairFromResponseObject = (object) => {
    let authToken = this._getTokenFromResponse(this.AUTH_TOKEN_NAME_IN_RESPONSE, object.body);
    let refreshToken = this._getTokenFromResponse(this.REFRESH_TOKEN_NAME_IN_RESPONSE, object.body);

    this._setTokenPair(authToken, refreshToken);
  }

  _login = (username, password) => {
    return this._authFetch(this.LOGIN_ENDPOINT, {
      method: 'POST',
      body: JSON.stringify({
        username,
        password
      })
    }).then(response => response.json())
      .then(res => {
        let authToken = this._getTokenFromResponse(this.AUTH_TOKEN_NAME_IN_RESPONSE, res);
        let refreshToken = this._getTokenFromResponse(this.REFRESH_TOKEN_NAME_IN_RESPONSE, res);
        if (authToken !== undefined && refreshToken !== undefined) {
          this._setTokenPair(authToken, refreshToken);
          return {result: true};
        } else {
          this._removeTokens(
          [this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE,
           this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE]
          );
          return {result: false, errors: res['response']['errors']};
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
          return {result: false, errors: res_json['response']['errors']};
        })
      }
    })
  };

  _getTokenFromResponse = (tokenName, responseObject) => {
    return responseObject?.response?.user?.[tokenName];
  }

  _authFetch = (url, options = {}) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this.loggedIn()) {
      headers['Authentication-Token'] = this._getToken(this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE);
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
          this._removeTokens([this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE]);
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
    const token = this._getToken(this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE);
    return (token !== null);
  }

  _setTokenPair(authToken, refreshToken) {
    localStorage.setItem(this.AUTH_TOKEN_NAME_IN_LOCALSTORAGE, authToken);
    localStorage.setItem(this.REFRESH_TOKEN_NAME_IN_LOCALSTORAGE, refreshToken);
  }

  _removeTokens(tokenNameArray) {
      tokenNameArray?.forEach(tokenName => {
        localStorage.removeItem(tokenName);
      })
  }

  _getToken(tokenName) {
    return localStorage.getItem(tokenName)
  }

}
