import React from 'react';
import {Col} from 'react-bootstrap';

import AuthService from '../../services/AuthService'

class LoginPageComponent extends React.Component {
  login = () => {
    this.auth.login(this.username, this.password).then(res => {
      if (res['result']) {
        this.redirectToHome();
      } else {
        this.setState({failed: true});
      }
    });
  };

  updateUsername = (evt) => {
    this.username = evt.target.value;
  };

  updatePassword = (evt) => {
    this.password = evt.target.value;
  };

  redirectToHome = () => {
    window.location.href = '/';
  };

  constructor(props) {
    super(props);
    this.username = '';
    this.password = '';
    this.auth = new AuthService();
    this.state = {
      failed: false
    };
    if (this.auth.loggedIn()) {
      this.redirectToHome();
    }
  }

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">Login</h1>
        <div className="col-sm-6 col-sm-offset-3" style={{'fontSize': '1.2em'}}>
          <div className="panel panel-default">
            <div className="panel-heading text-center">
              <b>Login</b>
            </div>
            <div className="panel-body">
              <div className="input-group center-block text-center">
                <input type="text" className="form-control" placeholder="Username"
                       onChange={evt => this.updateUsername(evt)}/>
                <input type="password" className="form-control" placeholder="Password"
                       onChange={evt => this.updatePassword(evt)}/>
                <button type="button" className="btn btn-primary btn-lg" style={{margin: '5px'}}
                        onClick={() => {
                          this.login()
                        }}>
                  Login
                </button>
                {
                  this.state.failed ?
                    <div className="alert alert-danger" role="alert">Login failed. Bad credentials.</div>
                    :
                    ''
                }
              </div>
            </div>
          </div>
        </div>
      </Col>
    );
  }
}

export default LoginPageComponent;
