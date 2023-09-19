import React from 'react';
import {Row, Col, Container, Form, Button} from 'react-bootstrap';

import AuthService, {getErrors} from '../../services/AuthService';
import monkeyDetective from '../../images/detective-monkey.svg';
import ParticleBackground from '../ui-components/ParticleBackground';
import LoadingIcon from '../ui-components/LoadingIcon';

class RegisterPageComponent extends React.Component {

  register = (event) => {
    event.preventDefault();
    this.setState({loading: true})
    this.auth.register(this.username, this.password).then(res => {
      this.setState({failed: false, error: ''});
      if (res['result']) {
        this.redirectToHome();
      } else {
        this.setState({
          loading: false,
          failed: true,
          errors: res['errors']
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
      <Container fluid className={'auth-container'}>
        <ParticleBackground />
        <Row>
          <Col xs={12} lg={{span: 6, offset: 3}} md={{span: 7, offset: 3}}
               className={'auth-block'}>
            <Row>
              <Col lg={8} md={8} sm={8}>
                <h1 className='reg-title'>First time?</h1>
                <h3 className='reg-subtitle'>Register a user</h3>
                <div>
                  <Form className={'auth-form'} onSubmit={this.register} >
                    <Form.Control onChange={evt => this.updateUsername(evt)} type='text' placeholder='Username'/>
                    <Form.Control onChange={evt => this.updatePassword(evt)} type='password' placeholder='Password'/>
                    <Button className={'monkey-submit-button'} type={'submit'} >
                      {
                        this.state.loading ?
                          <LoadingIcon/>
                          :
                          'Let\'s go!'
                      }
                    </Button>
                    <Row>
                      <Col>
                        {
                          this.state.failed ?
                            <div className='alert alert-danger' role='alert'>{getErrors(this.state.errors)}</div>
                            :
                            ''
                        }
                      </Col>
                    </Row>
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
