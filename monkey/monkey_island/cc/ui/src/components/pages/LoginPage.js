import React from 'react';
import {Col} from 'react-bootstrap';

import AuthService from '../../services/AuthService';

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

  redirectToRegistration = () => {
    window.location.href = '/register';
  };

  constructor(props) {
    super(props);
    this.username = '';
    this.password = '';
    this.auth = new AuthService();
    this.state = {
      failed: false
    };

    this.auth.needsRegistration()
      .then(result => {
        if(result){
          this.redirectToRegistration()
        }
      })
    this.auth.loggedIn()
      .then(res => {
        if (res) {
          this.redirectToHome();
        }
      });
  }

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">Login</h1>
        <div style={{'fontSize': '1.2em'}}>
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
