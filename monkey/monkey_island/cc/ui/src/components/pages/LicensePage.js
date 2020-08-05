import React from 'react';
import {Col} from 'react-bootstrap';
import rainge from 'rainge';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCopyright} from '@fortawesome/free-regular-svg-icons';

class LicensePageComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  setSelectedSection = (key) => {
    this.setState({
      selectedSection: key
    });
  };

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">License</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            Copyright <FontAwesomeIcon icon={faCopyright}/> {rainge(2015)} Guardicore Ltd.
            <br/>
            Licensed under <a href="https://www.gnu.org/licenses/gpl-3.0.html" rel="noopener noreferrer" target="_blank">GPLv3</a>.
          </p>
          <p>
            The source code is available on <a href="https://github.com/guardicore/monkey" rel="noopener noreferrer" target="_blank">GitHub</a>
          </p>
        </div>
      </Col>
    );
  }
}

export default LicensePageComponent;
