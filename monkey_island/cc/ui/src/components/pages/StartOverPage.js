import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {ModalContainer, ModalDialog} from 'react-modal-dialog';

class StartOverPageComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      cleaned: false,
      showCleanDialog: false,
      allMonkeysAreDead: false
    };
  }

  updateMonkeysRunning = () => {
    fetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done'])
        });
      });
  };

  renderCleanDialogModal = () => {
    if (!this.state.showCleanDialog) {
      return <div />
    }

    return (
      <ModalContainer onClose={() => this.setState({showCleanDialog: false})}>
        <ModalDialog onClose={() => this.setState({showCleanDialog: false})}>
          <h1>Reset environment</h1>
          <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
            Are you sure you want to reset the environment?
          </p>
          {
            !this.state.allMonkeysAreDead ?
              <div className="alert alert-warning">
                <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
                Some monkeys are still running. It's advised to kill all monkeys before resetting.
              </div>
              :
              <div />
          }
          <button type="button" className="btn btn-danger btn-lg" style={{margin: '5px'}}
                  onClick={() => {
                    this.cleanup();
                    this.setState({showCleanDialog: false});
                  }}>
            Reset environment
          </button>
          <button type="button" className="btn btn-success btn-lg" style={{margin: '5px'}}
                  onClick={() => this.setState({showCleanDialog: false})}>
            Cancel
          </button>
        </ModalDialog>
      </ModalContainer>
    )
  };

  render() {
    return (
      <Col xs={8}>
        {this.renderCleanDialogModal()}
        <h1 className="page-title">Start Over</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            In order to reset the entire environment, all monkeys will be ordered to kill themselves
            and the database will be cleaned up.
          </p>
          <p>
            After that you could go back to the <Link to="/run-monkey">Run Monkey</Link> page to start new infections.
          </p>
          <p style={{margin: '20px'}}>
            <button className="btn btn-danger btn-lg center-block"
                    onClick={() => {
                      this.setState({showCleanDialog: true});
                      this.updateMonkeysRunning();}
                    }>
              Reset Environment
            </button>
          </p>
          <div className="alert alert-info">
            <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
            You can continue and <Link to="/run-monkey">Run More Monkeys</Link> as you wish,
            and see the results on the <Link to="/infection/map">Infection Map</Link> without deleting anything.
          </div>
          { this.state.cleaned ?
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
    fetch('/api?action=reset')
      .then(res => res.json())
      .then(res => {
        if (res['status'] === 'OK') {
          this.setState({
              cleaned: true
            });
        }
      });
  }
}

export default StartOverPageComponent;
