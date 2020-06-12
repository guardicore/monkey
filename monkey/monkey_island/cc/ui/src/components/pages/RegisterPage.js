import React from 'react';
import {Col} from 'react-bootstrap';

import AuthService from '../../services/AuthService';

class RegisterPageComponent extends React.Component {

  register = () => {
    this.auth.register(this.username, this.password).then(res => {
      this.setState({failed: false, error: ""});
      if (res['result']) {
        this.redirectToHome();
      } else {
        this.setState({failed: true,
                            error: res['error']});
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
      failed: false,
      loading: false
    };

    this.auth.needsRegistration()
      .then(result => {
        if(!result){
          this.redirectToHome()
        }
      })
  }

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">First time?</h1>
        <h3 className="page-title">Let's secure your island</h3>
        <div className="col-sm-6 col-sm-offset-3" style={{'fontSize': '1.2em'}}>
          <div className="panel panel-default">
            <div className="panel-heading text-center">
              <b>Register</b>
            </div>
            <div className="panel-body">
              <div className="input-group center-block text-center">
                <input type="text" className="form-control" placeholder="Username"
                       onChange={evt => this.updateUsername(evt)}/>
                <input type="password" className="form-control" placeholder="Password"
                       onChange={evt => this.updatePassword(evt)}/>
                <button type="button" className="btn btn-primary btn-lg" style={{margin: '5px'}}
                        onClick={() => {
                          this.register()
                        }}>
                  Lets Go!
                </button>
                {
                  this.state.failed ?
                    <div className="alert alert-danger" role="alert">{this.state.error}</div>
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

export default RegisterPageComponent;
