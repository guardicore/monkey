import React from 'react';
import {Button, Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';

class AttackReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title no-print">5.ATT&CK techniques report</h1>
        <div style={{'fontSize': '1.2em'}}>
          ATT&CK techniques report
        </div>
      </Col>
    );
  }
}

export default AttackReportPageComponent;
