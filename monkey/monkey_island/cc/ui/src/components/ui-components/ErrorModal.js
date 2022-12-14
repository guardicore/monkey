import {Modal} from 'react-bootstrap';
import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';


class ErrorModal extends React.PureComponent {

  constructor(props) {
    super(props);

    this.state = {
      showModal: this.props.showModal,
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props !== prevProps) {
      this.setState({
        showModal: this.props.showModal
      })
    }
  }

  render = () => {
    return (
      <Modal show={this.state.showModal} onHide={() => this.props.onClose()}>
        <Modal.Header closeButton>
          <Modal.Title> Uh oh... </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
            <div className="alert alert-danger">
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              {this.props.errorMessage}
            </div>
          </div>
          {this.props.errorDetails !== undefined &&
            <div>
              <hr/>
              <h4>Error Details</h4>
              <p style={{'word-wrap': 'break-word'}}>
                {this.props.errorDetails}
              </p>
            </div>
          }
        </Modal.Body>
      </Modal>
    )
  };
}

export default ErrorModal;
