import React from 'react';
import {Col} from 'react-bootstrap';

class ReportPageComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Col xs={12}>
        <h1 className="page-title">Penetration Test Report</h1>
        <div style={{'fontSize': '1.5em'}}>
          <p>
            Under construction
          </p>
        </div>
      </Col>
    );
  }
}

export default ReportPageComponent;
