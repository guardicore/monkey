import {Modal} from 'react-bootstrap';
import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';


class Error404Modal extends React.PureComponent {

  constructor(props) {
    super(props);

    this.state = {
      showModal: this.props.showModal
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
            <p className="alert alert-danger">
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              The server returned a 404 (NOT FOUND) response.
            </p>
          </div>
        </Modal.Body>
      </Modal>
    )
  };
}

export default Error404Modal;
