import React from 'react';
import {Button, Col, Row} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faSync} from '@fortawesome/free-solid-svg-icons/faSync';
import AuthComponent from '../../AuthComponent';

import MissingBinariesModal from '../../ui-components/MissingBinariesModal';
import '../../../styles/components/RunOnIslandButton.scss';


class RunOnIslandButton extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      runningOnIslandState: 'not_running',
      showModal: false,
      errorDetails: ''
    };

    this.closeModal = this.closeModal.bind(this);
  }

  componentDidMount() {
    this.authFetch('/api/local-monkey')
      .then(res => res.json())
      .then(res => {
        if (res['is_running']) {
          this.setState({runningOnIslandState: 'running'});
        } else {
          this.setState({runningOnIslandState: 'not_running'});
        }
      });
  }

  runIslandMonkey = () => {
    this.setState({runningOnIslandState: 'installing'}, this.sendRunMonkeyRequest)

  };

  sendRunMonkeyRequest = () => {
    this.authFetch('/api/local-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'run'})
      })
      .then(res => res.json())
      .then(res => {
        if (res['is_running']) {
          this.setState({
            runningOnIslandState: 'running'
          });
        } else {
          /* If Monkey binaries are missing, change the state accordingly */
          if (res['error_text'].startsWith('Copy file failed')) {
            this.setState({
                showModal: true,
                errorDetails: res['error_text']
              }
            );
          }
          this.setState({
            runningOnIslandState: 'not_running'
          });
        }
      });
  }

  closeModal = () => {
    this.setState({
      showModal: false
    })
  };

  getMonkeyRunStateIcon = () => {
    if (this.state.runningOnIslandState === 'running') {
      return (<FontAwesomeIcon icon={faCheck}
                               className={`monkey-on-island-run-state-icon text-success`}/>)
    } else if (this.state.runningOnIslandState === 'installing') {
      return (<FontAwesomeIcon icon={faSync}
                               className={`monkey-on-island-run-state-icon text-success spinning-icon`}/>)
    } else {
      return '';
    }
  }

  render() {
    let description = this.props.description !== undefined ? (<p>{this.props.description}</p>) : ''
    let icon = this.props.icon !== undefined ? (<FontAwesomeIcon icon={this.props.icon}/>) : ''
    return (
      <Row>
        <Col>
          <MissingBinariesModal
            showModal={this.state.showModal}
            onClose={this.closeModal}
            errorDetails={this.state.errorDetails}/>
          <Button variant={'outline-monkey'} size='lg' className={'selection-button'}
                  onClick={this.runIslandMonkey}>
            {icon}
            <h1>{this.props.title}</h1>
            {description}
            {this.getMonkeyRunStateIcon()}
          </Button>
        </Col>
      </Row>
    );
  }
}

export default RunOnIslandButton;
