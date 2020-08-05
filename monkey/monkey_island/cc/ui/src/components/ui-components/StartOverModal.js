import {Modal} from 'react-bootstrap';
import React from 'react';
import {GridLoader} from 'react-spinners';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';


class StartOverModal extends React.PureComponent {

  constructor(props) {
    super(props);

    this.state = {
      showCleanDialog: this.props.showCleanDialog,
      allMonkeysAreDead: this.props.allMonkeysAreDead,
      loading: false
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props !== prevProps) {
      this.setState({ showCleanDialog: this.props.showCleanDialog,
                      allMonkeysAreDead: this.props.allMonkeysAreDead})
    }
  }

  render = () => {
    return (
      <Modal show={this.state.showCleanDialog} onHide={() => this.props.onClose()}>
        <Modal.Body>
          <h2>
            <div className='text-center'>Reset environment</div>
          </h2>
          <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
            Are you sure you want to reset the environment?
          </p>
          {
            !this.state.allMonkeysAreDead ?
              <div className='alert alert-warning'>
                <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
                Some monkeys are still running. It's advised to kill all monkeys before resetting.
              </div>
              :
              <div/>
          }
          {
            this.state.loading ? <div className={'modalLoader'}><GridLoader/></div> : this.showModalButtons()
          }
        </Modal.Body>
      </Modal>
    )
  };

  showModalButtons() {
    return (<div className='text-center'>
              <button type='button' className='btn btn-danger btn-lg' style={{margin: '5px'}}
                      onClick={this.modalVerificationOnClick}>
                Reset environment
              </button>
              <button type='button' className='btn btn-success btn-lg' style={{margin: '5px'}}
                      onClick={() => {this.props.onClose(); this.setState({showCleanDialog: false})}}>
                Cancel
              </button>
            </div>)
  }

  modalVerificationOnClick = async () => {
    this.setState({loading: true});
    this.props.onVerify()
      .then(() => {this.setState({loading: false});
                   this.props.onClose();})

  }
}

export default StartOverModal;
