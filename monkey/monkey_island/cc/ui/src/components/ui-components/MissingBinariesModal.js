import {Modal} from 'react-bootstrap';
import React from 'react';
import {GridLoader} from 'react-spinners';


class MissingBinariesModal extends React.PureComponent {

  constructor(props) {
    super(props);

    this.state = {
      showModal: this.props.showModal,
      errorDetails: this.props.errorDetails
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props !== prevProps) {
      this.setState({
        showModal: this.props.showModal,
        errorDetails: this.props.errorDetails
      })
    }
  }

  render = () => {
    return (
      <Modal show={this.state.showModal} onHide={() => this.props.onClose()}>
        <Modal.Body>
          <h3>
            <div className='text-center'>Uh oh...</div>
          </h3>
          <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
            <p className="alert alert-warning">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              Some Monkey binaries are not found where they should be...<br/>
              You can download the files from <a href="https://github.com/guardicore/monkey/releases/latest" target="blank">here</a>,
              at the bottommost section titled "Assets", and place them under the directory <code>monkey/monkey_island/cc/binaries</code>.
            </p>
          </div>
          <hr/>
          <h4>
            Error Details
          </h4>
          <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
            <pre>
              {this.state.errorDetails}
            </pre>
          </div>
          <div className='text-center'>
            <button type='button' className='btn btn-success btn-lg' style={{margin: '5px'}}
                    onClick={() => this.props.onClose()}>
              Dismiss
            </button>
          </div>
        </Modal.Body>
      </Modal>
    )
  };

}

export default MissingBinariesModal;
