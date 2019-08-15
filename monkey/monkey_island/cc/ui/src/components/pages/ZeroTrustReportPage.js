import React from 'react';
import {Button, Col, Row, Grid} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from "../report-components/common/ReportHeader";
import PillarsOverview from "../report-components/zerotrust/PillarOverview";
import FindingsTable from "../report-components/zerotrust/FindingsTable";
import {SinglePillarDirectivesStatus} from "../report-components/zerotrust/SinglePillarDirectivesStatus";
import {MonkeysStillAliveWarning} from "../report-components/common/MonkeysStillAliveWarning";
import ReportLoader from "../report-components/common/ReportLoader";
import MustRunMonkeyWarning from "../report-components/common/MustRunMonkeyWarning";
import {SecurityIssuesGlance} from "../report-components/common/SecurityIssuesGlance";
import {StatusesToPillarsSummary} from "../report-components/zerotrust/StatusesToPillarsSummary";

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  componentDidMount() {
    this.updateMonkeysRunning().then(res => this.getZeroTrustReportFromServer(res));
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done']),
          runStarted: res['completed_steps']['run_monkey']
        });
        return res;
      });
  };

  render() {
    let content;
    if (this.state.runStarted) {
      content = this.generateReportContent();
    } else {
      content = <MustRunMonkeyWarning/>;
    }

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

    if (this.stillLoadingDataFromServer()) {
      content = <ReportLoader loading={true}/>;
    } else {
      const overviewSection = <div id="overview-section">
        <h2>Overview</h2>
        <Grid fluid={true}>
          <Row className="show-grid">
            <Col xs={8} sm={8} md={8} lg={8}>
              <PillarsOverview pillarsToStatuses={this.state.pillars.pillarsToStatuses} grades={this.state.pillars.grades}/>
            </Col>
            <Col xs={4} sm={4} md={4} lg={4}>
              <MonkeysStillAliveWarning allMonkeysAreDead={this.state.allMonkeysAreDead}/>
              <SecurityIssuesGlance issuesFound={this.anyIssuesFound()}/>
              <StatusesToPillarsSummary statusesToPillars={this.state.pillars.statusesToPillars} />
            </Col>
          </Row>
        </Grid>
      </div>;

      const directivesSection = <div id="directives-overview">
        <h2>Directives</h2>
        {
          Object.keys(this.state.directives).map((pillar) =>
            <SinglePillarDirectivesStatus
              key={pillar}
              pillar={pillar}
              directivesStatus={this.state.directives[pillar]}/>
          )
        }
      </div>;

      const findingSection = <div id="findings-overview">
        <h2>Findings</h2>
        <FindingsTable pillarsToStatuses={this.state.pillars.pillarsToStatuses} findings={this.state.findings}/>
      </div>;

      content = <div id="MainContentSection">
        {overviewSection}
        {directivesSection}
        {findingSection}
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
        </div>
      </div>
    )
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined" || typeof this.state.pillars === "undefined" || typeof this.state.directives === "undefined";
  }

  print() {
    alert("unimplemented");
  }

  getZeroTrustReportFromServer() {
    let res;
    this.authFetch('/api/report/zero_trust/findings')
      .then(res => res.json())
      .then(res => {
        this.setState({
          findings: res
        });
      });
    this.authFetch('/api/report/zero_trust/directives')
      .then(res => res.json())
      .then(res => {
        this.setState({
          directives: res
        });
      });
    this.authFetch('/api/report/zero_trust/pillars')
      .then(res => res.json())
      .then(res => {
        this.setState({
          pillars: res
        });
      });
  }

  anyIssuesFound() {
    const severe = function(finding) {
      return (finding.status === "Conclusive" || finding.status === "Inconclusive");
    };

    return this.state.findings.some(severe);
  }
}

export default ZeroTrustReportPageComponent;
