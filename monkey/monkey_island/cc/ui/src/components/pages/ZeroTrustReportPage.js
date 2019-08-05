import React from 'react';
import {Button, Col} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, { ReportTypes } from "../report-components/common/ReportHeader";
import ZeroTrustReportPillarGrades from "../report-components/zerotrust/ZeroTrustReportPillarGrades";

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      report: {
        findings: undefined
      },
      allMonkeysAreDead: false,
      runStarted: false
    };
  }

  render() {
    let res;
    this.getZeroTrustReportFromServer(res);

    const content = this.generateReportContent();

    return (
      <Col xs={12} lg={10}>
        <h1 className="page-title no-print">5. Zero Trust Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }

  generateReportContent() {
    let content;

    console.log(this.state.report.findings);

    if (typeof this.state.report.findings === "undefined") {
      content = "Still empty";
    } else {
      content = <div>
        <ZeroTrustReportPillarGrades findings={this.state.report.findings} />
      </div>;
    }

    return (
      <div>
        <div className="text-center no-print" style={{marginBottom: '20px'}}>
          <Button bsSize="large" onClick={() => {
            this.print();
          }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
        </div>

        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
          THIS IS THE RAW SERVER DATA
          <pre id="json-report">
            {JSON.stringify(this.state.report, undefined, 2)}
          </pre>
        </div>
      </div>
    )
  }

  print() {
    alert("unimplemented");
  }

  getZeroTrustReportFromServer() {
    this.authFetch('/api/report/zero_trust')
      .then(res => res.json())
      .then(res => {
        this.setState({
          report: res
        });
      });
  }
}

export default ZeroTrustReportPageComponent;
