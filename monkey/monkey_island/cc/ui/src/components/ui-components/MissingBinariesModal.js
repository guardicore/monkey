import {Modal} from 'react-bootstrap';
import React from 'react';
import {GridLoader} from 'react-spinners';


class MissingBinariesModal extends React.PureComponent {

  constructor(props) {
    super(props);

    this.state = {
      showModal: this.props.showModal
    };
  }

  render = () => {
    return (
      <Modal show={this.props.showModal} onHide={() => this.props.onClose()}>
        <Modal.Body>
          <h3>
            <div className='text-center'>Uh oh...</div>
          </h3>
          <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
            Some Monkey binaries are not found where they should be...{"\r\n"}
            Try downloading them from <a href="https://github.com/guardicore/monkey/releases/latest" target="blank">here</a>,
            at the bottommost section titled "Assets".
          </p>
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
