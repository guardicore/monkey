import React from 'react';
import {Button, Col, Container, Form, Row} from 'react-bootstrap';

import AuthService from '../../services/AuthService';
import monkeyGeneral from '../../images/militant-monkey.svg';
import ParticleBackground from '../ui-components/ParticleBackground';

class LoginPageComponent extends React.Component {
  login = (event) => {
    event.preventDefault()
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
        if (result) {
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
      <Container fluid className={'auth-container'}>
        <ParticleBackground/>
        <Row>
          <Col xs={12} lg={{span: 6, offset: 3}} md={{span: 7, offset: 3}} className={'auth-block'}>
            <Row>
              <Col lg={8} md={8} sm={8}>
                <h1 className='auth-title'>Login</h1>
                <div>
                  <Form className={'auth-form'} onSubmit={this.login}>
                    <Form.Control onChange={evt => this.updateUsername(evt)} type='text' placeholder='Username'/>
                    <Form.Control onChange={evt => this.updatePassword(evt)} type='password' placeholder='Password'/>
                    <Button id={'auth-button'} type={'submit'}>
                      Login
                    </Button>
                    {
                      this.state.failed ?
                        <div className="alert alert-danger" role="alert">Login failed. Bad credentials.</div>
                        :
                        ''
                    }
                  </Form>
                </div>
              </Col>
              <Col lg={4} md={4} sm={4}>
                <img alt="infection monkey" className={'monkey-detective'} src={monkeyGeneral}/>
              </Col>
            </Row>
          </Col>
        </Row>
      </Container>)
  }
}

export default LoginPageComponent;
