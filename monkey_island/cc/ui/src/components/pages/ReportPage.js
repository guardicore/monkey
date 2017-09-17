import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';

class ReportPageComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Penetration Test Report</h1>
        <div style={{'fontSize': '1.5em'}}>
          <p>
            In order to reset the entire environment, all monkeys will be ordered to kill themselves
            and the database will be cleaned up.
          </p>
          <p>
            After that you could go back to the <Link to="/run-monkey">Run Monkey</Link> page to start new infections.
          </p>
          <p>
            <a onClick={this.cleanup} className="btn btn-danger">Reset Environment</a>
          </p>
        </div>
      </Col>
    );
  }
}

export default ReportPageComponent;
