import React from 'react';
import {Col} from 'react-bootstrap';

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
      <Col xs={12} lg={8}>
        <h1 className="page-title">License</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            Copyright <i className="glyphicon glyphicon-copyright-mark"/> 2017 Guardicore Ltd.
            <br/>
            Licensed under <a href="https://www.gnu.org/licenses/gpl-3.0.html" target="_blank">GPLv3</a>.
          </p>
          <p>
            The source code is available on <a href="https://github.com/guardicore/monkey" target="_blank">GitHub</a>
          </p>
        </div>
      </Col>
    );
  }
}

export default LicensePageComponent;
