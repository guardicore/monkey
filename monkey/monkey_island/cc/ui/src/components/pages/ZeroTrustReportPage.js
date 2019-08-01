import React from 'react';
import {Button, Col} from 'react-bootstrap';
import BreachedServers from 'components/report-components/BreachedServers';
import ScannedServers from 'components/report-components/ScannedServers';
import PostBreach from 'components/report-components/PostBreach';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/StolenPasswords';
import CollapsibleWellComponent from 'components/report-components/CollapsibleWell';
import {Line} from 'rc-progress';
import AuthComponent from '../AuthComponent';
import PassTheHashMapPageComponent from "./PassTheHashMapPage";
import StrongUsers from "components/report-components/StrongUsers";
import AttackReport from "components/report-components/AttackReport";

let guardicoreLogoImage = require('../../images/guardicore-logo.png');
let monkeyLogoImage = require('../../images/monkey-icon.svg');

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      report: {},
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  render() {
    let content;
    let res;
    this.getZeroTrustReportFromServer(res);
    content = JSON.stringify(this.state.report);

    return (
      <Col xs={12} lg={10}>
        <h1 className="page-title no-print">4. Security Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }

  // This dups the regular report
  getZeroTrustReportFromServer(res) {
    //if (res['completed_steps']['run_monkey']) {
      this.authFetch('/api/report/zero_trust')
        .then(res => res.json())
        .then(res => {
          this.setState({
            report: res
          });
        });
    //}
  }
}

export default ZeroTrustReportPageComponent;
