import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import AuthComponent from '../AuthComponent';
import StartOverModal from '../ui-components/StartOverModal';
import '../../styles/StartOverPage.scss';

class StartOverPageComponent extends AuthComponent {
  constructor(props) {
    super(props);

    this.state = {
      cleaned: false,
      showCleanDialog: false,
      allMonkeysAreDead: false
    };

    this.cleanup = this.cleanup.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  updateMonkeysRunning = () => {
    this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done'])
        });
      });
  };

  render() {
    return (
      <Col xs={12} lg={8}>
        <StartOverModal cleaned = {this.state.cleaned}
                        showCleanDialog = {this.state.showCleanDialog}
                        allMonkeysAreDead = {this.state.allMonkeysAreDead}
                        onVerify = {this.cleanup}
                        onClose = {this.closeModal}/>
        <h1 className="page-title">Start Over</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            If you are finished and want to start over with a fresh configuration, erase the logs and clear the map
            you can go ahead and
          </p>
          <p style={{margin: '20px'}}>
            <button className="btn btn-danger btn-lg center-block"
                    onClick={() => {
                      this.setState({showCleanDialog: true});
                      this.updateMonkeysRunning();
                    }
                    }>
              Reset the Environment
            </button>
          </p>
          <div className="alert alert-info">
            <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
            You don't have to reset the environment to keep running monkeys.
            You can continue and <Link to="/run-monkey">Run More Monkeys</Link> as you wish,
            and see the results on the <Link to="/infection/map">Infection Map</Link> without deleting anything.
          </div>
          {this.state.cleaned ?
            <div className="alert alert-success">
              <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
              Environment was reset successfully
            </div>
            : ''}
        </div>
      </Col>
    );
  }

  cleanup = () => {
    this.setState({
      cleaned: false
    });
    return this.authFetch('/api?action=reset')
      .then(res => res.json())
      .then(res => {
        if (res['status'] === 'OK') {
          this.setState({
            cleaned: true
          });
        }
      }).then(this.updateMonkeysRunning());
  };

  closeModal = () => {
    this.setState({
      showCleanDialog: false,
    })
  };
}

export default StartOverPageComponent;
