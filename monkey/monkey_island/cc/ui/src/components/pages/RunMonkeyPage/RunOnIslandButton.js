import React from 'react';
import {Button, Col, Row} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faSync} from '@fortawesome/free-solid-svg-icons/faSync';
import AuthComponent from '../../AuthComponent';

import IslandMonkeyRunErrorModal from '../../ui-components/IslandMonkeyRunErrorModal';
import '../../../styles/components/RunOnIslandButton.scss';
import {faTimes} from '@fortawesome/free-solid-svg-icons';
import IslandHttpClient, {APIEndpoint} from '../../IslandHttpClient';


const MONKEY_STATES = {
  RUNNING: 'running',
  NOT_RUNNING: 'not_running',
  STARTING: 'starting',
  FAILED: 'failed'
}

class RunOnIslandButton extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      // TODO: Can't we just use true/false for this?
      runningOnIslandState: MONKEY_STATES.NOT_RUNNING,
      showModal: false,
      errorDetails: ''
    };

    this.closeModal = this.closeModal.bind(this);
  }

  componentDidMount() {
    IslandHttpClient.get(APIEndpoint.machines).then(res => {
      const island_machine_id = this.get_island_machine_id(res.body)

      IslandHttpClient.get(APIEndpoint.agents).then(res => {
        if (this.agents_running_on_machine(island_machine_id, res.body)) {
          this.setState({runningOnIslandState: MONKEY_STATES.RUNNING});
        } else {
          this.setState({runningOnIslandState: MONKEY_STATES.NOT_RUNNING});
        }
      })
    })

  }

  get_island_machine_id(machines) {
      for (const i in machines) {
        if (machines[i].island === true) {
          return machines[i].id
        }
      }
  }

  agents_running_on_machine(machine_id, agents) {
    for (const i in agents) {
      if (agents[i].machine_id !== machine_id) {
        continue;
      }

      if (agents[i].stop_time === null) {
        return true;
      }
    }

    return false;
  }


  runIslandMonkey = () => {
    this.setState({runningOnIslandState: MONKEY_STATES.STARTING}, this.sendRunMonkeyRequest)

  };

  sendRunMonkeyRequest() {
    this.authFetch('/api/local-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'run'})
      })
      .then(res => res.json())
      .then(async res => {
        if (res['is_running']) {
          await new Promise(r => setTimeout(r, 1000));
          this.setState({
            runningOnIslandState: MONKEY_STATES.RUNNING
          });
        } else {
          /* If Monkey binaries are missing, change the state accordingly */
          if (res['error_text'] !== '') {
            this.setState({
                showModal: true,
                errorDetails: res['error_text'],
                runningOnIslandState: MONKEY_STATES.FAILED
              }
            );
          }
        }
      });
  }

  closeModal = () => {
    this.setState({
      showModal: false
    })
  };

  getMonkeyRunStateIcon = () => {
    if (this.state.runningOnIslandState === MONKEY_STATES.RUNNING) {
      return (<FontAwesomeIcon icon={faCheck}
                               className={`monkey-on-island-run-state-icon text-success`}/>)
    } else if (this.state.runningOnIslandState === MONKEY_STATES.STARTING) {
      return (<FontAwesomeIcon icon={faSync}
                               className={`monkey-on-island-run-state-icon text-success spinning-icon`}/>)
    } else if (this.state.runningOnIslandState === MONKEY_STATES.FAILED) {
      return (<FontAwesomeIcon icon={faTimes}
                               className={`monkey-on-island-run-state-icon text-danger`}/>)
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
          <IslandMonkeyRunErrorModal
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
