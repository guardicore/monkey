import React, {Component} from 'react';
import {Col} from 'react-bootstrap';
import * as PropTypes from 'prop-types';

import monkeyLogoImage from '../../../images/monkey-icon.svg';

export const ReportTypes = {
  zeroTrust: 'Zero Trust',
  security: 'Security',
  attack: 'ATT&CK',
  null: ''
};

export class ReportHeader extends Component {
  report_type;

  render() {
    return <div id="header" className="row justify-content-between">
      <Col xs={8}>
        <div>
          <h1 style={{marginTop: '0px', marginBottom: '5px', color: '#666666', fontFamily: 'Alegreya'}}>
            {this.props.report_type} Report</h1>
          <h1 style={{
            marginTop: '0px',
            marginBottom: '0px',
            color: '#ffcc00',
            fontFamily: 'Alegreya'
          }}>Infection <b>Monkey</b></h1>
        </div>
      </Col>
      <Col xs={4}>
        <img alt="monkey logo image" src={monkeyLogoImage}
             style={{
               float: 'right',
               width: '80px'
             }}/>
      </Col>
    </div>
  }
}

export default ReportHeader;

ReportHeader.propTypes = {
  report_type: PropTypes.string
};
