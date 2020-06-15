import React from 'react';
import {Row, Col, Container, Form, Button} from 'react-bootstrap';
import Particles from 'react-particles-js';

import AuthService from '../../services/AuthService';
import '../../styles/RegisterPage.scss';
import {particleParams} from '../../styles/particle-component/RegistrationPageParams';
import monkeyDetective from '../../images/detective-monkey.svg';

class RegisterPageComponent extends React.Component {

  register = () => {
    this.auth.register(this.username, this.password).then(res => {
      this.setState({failed: false, error: ''});
      if (res['result']) {
        this.redirectToHome();
      } else {
        this.setState({
          failed: true,
          error: res['error']
        });
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
        if (!result) {
          this.redirectToHome()
        }
      })
  }

  render() {
    return (
      <Container fluid className={'registration-container'}>
        <Particles className={'particle-background'} params={particleParams}/>
        <Row>
          <Col xs={12} lg={{span: 6, offset: 3}} md={{span: 7, offset: 3}} className={'registration-block'}>
            <Row>
              <Col lg={8} md={8} sm={8}>
                <h1 className='reg-title'>First time?</h1>
                <h3 className='reg-subtitle'>Let's secure your island!</h3>
                <div>
                  <Form className={'registration-form'}>
                    <Form.Control onChange={evt => this.updateUsername(evt)} type='text' placeholder='Username'/>
                    <Form.Control onChange={evt => this.updatePassword(evt)} type='password' placeholder='Password'/>
                    <Button id={'registration-button'} onClick={() => {
                      this.register()
                    }}>
                      Lets Go!
                    </Button>
                    {
                      this.state.failed ?
                        <div className='alert alert-danger' role='alert'>{this.state.error}</div>
                        :
                        ''
                    }
                  </Form>
                </div>
              </Col>
              <Col lg={4} md={4} sm={4}>
                <img alt="infection monkey" className={'monkey-detective'} src={monkeyDetective}/>
              </Col>
            </Row>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default RegisterPageComponent;
