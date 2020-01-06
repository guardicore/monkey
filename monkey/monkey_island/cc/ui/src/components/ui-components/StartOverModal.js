import {Modal} from "react-bootstrap";
import Modal from "react-bootstrap/es/Modal";
import ReactComponent from "react";
import AuthComponent from "../AuthComponent";


class StartOverModal extends ReactComponent {
  render = () => {
    return (
      <Modal show={this.state.showCleanDialog} onHide={() => this.setState({showCleanDialog: false})}>
        <Modal.Body>
          <h2>
            <div className="text-center">Reset environment</div>
          </h2>
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
              <div/>
          }
          <div className="text-center">
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
          </div>
        </Modal.Body>
      </Modal>
    )

  };
}
