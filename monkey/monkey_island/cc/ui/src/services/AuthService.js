import React from 'react';
import {Mutex} from 'async-mutex';

const MUTEX = new Mutex();

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
  REFRESH_AUTH_TOKEN_ENDPOINT = '/api/refresh-authentication-token';

  TOKEN_NAME_IN_LOCALSTORAGE = 'authentication_token';
  TOKEN_NAME_IN_RESPONSE = 'authentication_token';

  TOKEN_TTL_NAME_IN_RESPONSE = 'token_ttl_sec';
  TOKEN_TTL_NAME_IN_LOCALSTORAGE = 'token_ttl_sec';

  login = (username, password) => {
    return this._login(username, password);
  };

  logout = () => {
    return this._authFetch(this.LOGOUT_ENDPOINT, {method: 'POST'})
      .then(response => response.json())
      .then(response => {
        if(response.meta.code === 200){
          this._removeAuthToken();
          this._removeAuthTokenExpirationTime();
        }
        return response;
      });
  }

  authFetch = (url, options, refreshToken = false) => {
    // `refreshToken` is a mechanism to prevent unneeded calls
    // to the refresh authentication token endpoint, such as when
    // the map page is left open but there's no other activity.

    // Before making the request, refresh the token if required.
    MUTEX.runExclusive(() => {
      if (refreshToken && this._shouldRefreshToken()) {
        this._refreshAuthToken();
      }
    });

    let authToken = this._getAuthToken();
    return MUTEX.runExclusive(() => {
        return this._doAuthFetch(url, options, authToken)
      }).then(res => {
        // If unauthorized, maybe the token was refreshed before the request
        // was processed. Get the token again from the storage (which will be
        // a new valid token if it was refreshed) and attempt the request again.
        // If it fails again as unauthorized, something else is up. Remove the invalid token.
        if (res.status === 401) {
            let latestAuthToken = this._getAuthToken();
            if (latestAuthToken != authToken) {
              return MUTEX.runExclusive(() => { return this._doAuthFetch(url, options, latestAuthToken); });
            }
            else {
              this._removeAuthToken();
              this._removeAuthTokenExpirationTime();
            }
        }
        return res;
    });
  };

  _refreshAuthToken = () => {
    this._fetchRefreshedAuthenticationToken()
      .then(response => response.json().then(data => ({status: response.status, body: data})))
      .then(object => {
        if(object.status === 200) {
          let authToken = this._getAuthTokenFromResponse(object.body);
          this._setAuthToken(authToken);
          let tokenExpirationTime = this._getAuthTokenExpirationTimeFromResponse(object.body);
          this._setAuthTokenExpirationTime(tokenExpirationTime);
        }
      })
  }

  _fetchRefreshedAuthenticationToken = () => {
    const options = {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authentication-Token': this._getAuthToken()
      }
    }
    return fetch(this.REFRESH_AUTH_TOKEN_ENDPOINT, options);
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
        let token = this._getAuthTokenFromResponse(res);
        if (token){
          this._setAuthToken(token);
          let tokenExpirationTime = this._getAuthTokenExpirationTimeFromResponse(res);
          this._setAuthTokenExpirationTime(tokenExpirationTime);
          return {result: true};
        } else {
          this._removeAuthToken();
          this._removeAuthTokenExpirationTime();
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

  _getAuthTokenFromResponse = (responseObject) => {
    return responseObject?.response?.user?.[this.TOKEN_NAME_IN_RESPONSE];
  }

  _getAuthTokenExpirationTimeFromResponse = (responseObject) => {
    return responseObject?.response?.user?.[this.TOKEN_TTL_NAME_IN_RESPONSE];
  }

  _authFetch = (url, options = {}) => {
    let token = this._getAuthToken();
    return this._doAuthFetch(url, options, token);
  };

  _doAuthFetch = (url, options, token) => {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    if (this.loggedIn()) {
      headers['Authentication-Token'] = token;
    }

    if (Object.prototype.hasOwnProperty.call(options, 'headers')) {
      if(this.loggedIn()){
        options['headers']['Authentication-Token'] = token;
      }
    } else {
      options['headers'] = {};
      for (let header in headers) {
        options['headers'][header] = headers[header];
      }
    }

    return fetch(url, options)
  }


  needsRegistration = () => {
    return fetch(this.REGISTRATION_STATUS_API_ENDPOINT,
      {method: 'GET'})
      .then(response => response.json())
      .then(res => {
        return res['needs_registration']
      })
  };

  loggedIn() {
    const token = this._getAuthToken();
    return (token !== null);
  }

  _setAuthToken(idToken) {
    localStorage.setItem(this.TOKEN_NAME_IN_LOCALSTORAGE, idToken);
  }

  _removeAuthToken() {
    localStorage.removeItem(this.TOKEN_NAME_IN_LOCALSTORAGE);
  }

  _getAuthToken() {
    return localStorage.getItem(this.TOKEN_NAME_IN_LOCALSTORAGE)
  }

  _setAuthTokenExpirationTime(tokenExpirationTime){
    let currentDateTimeSeconds = Date.now() / 1000;
    localStorage.setItem(this.TOKEN_TTL_NAME_IN_LOCALSTORAGE, currentDateTimeSeconds + (tokenExpirationTime * 0.7));
  }

  _removeAuthTokenExpirationTime(){
    localStorage.removeItem(this.TOKEN_TTL_NAME_IN_LOCALSTORAGE);
  }

  _getAuthTokenExpirationTime() {
    return localStorage.getItem(this.TOKEN_TTL_NAME_IN_LOCALSTORAGE);
  }

  _shouldRefreshToken = () => {
    let tokenExpirationTime = this._getAuthTokenExpirationTime();
    if(tokenExpirationTime) {
      let currentDateTime = Date.now() / 1000;
      return (tokenExpirationTime - currentDateTime) <= 0;
    }
    return false;
  }
}
