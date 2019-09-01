import React, {Fragment} from 'react';
import {Col, Grid, Row} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from "../report-components/common/ReportHeader";
import PillarsOverview from "../report-components/zerotrust/PillarOverview";
import FindingsSection from "../report-components/zerotrust/FindingsSection";
import SinglePillarRecommendationsStatus from "../report-components/zerotrust/SinglePillarRecommendationsStatus";
import MonkeysStillAliveWarning from "../report-components/common/MonkeysStillAliveWarning";
import ReportLoader from "../report-components/common/ReportLoader";
import MustRunMonkeyWarning from "../report-components/common/MustRunMonkeyWarning";
import PrintReportButton from "../report-components/common/PrintReportButton";
import {extractExecutionStatusFromServerResponse} from "../report-components/common/ExecutionStatus";
import ZeroTrustReportLegend from "../report-components/zerotrust/ReportLegend";

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  componentDidMount() {
    this.updatePageState();
    const refreshInterval = setInterval(this.updatePageState, 8000)
    this.setState(
      {refreshDataIntervalHandler: refreshInterval}
    )
  }

  componentWillUnmount() {
    clearInterval(this.state.refreshDataIntervalHandler);
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        this.setState(extractExecutionStatusFromServerResponse(res));
        return res;
      });
  };

  updatePageState = () => {
    this.updateMonkeysRunning().then(res => this.getZeroTrustReportFromServer(res));
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
      content = <div id="MainContentSection">
        {this.generateOverviewSection()}
        {this.generateRecommendationsSection()}
        {this.generateFindingsSection()}
      </div>;
    }

    return (
      <Fragment>
        <div style={{marginBottom: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
        </div>
        <div style={{marginTop: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
      </Fragment>
    )
  }

  generateOverviewSection() {
    return (<div id="overview-section">
      <h2>Summary</h2>
      <Grid fluid={true}>
        <Row>
          <Col xs={12} sm={12} md={12} lg={12}>
            <MonkeysStillAliveWarning allMonkeysAreDead={this.state.allMonkeysAreDead}/>
            <p>
              Get a quick glance of the status for each of Zero Trust's seven pillars.
            </p>
          </Col>
        </Row>
        <Row className="show-grid">
          <Col xs={8} sm={8} md={8} lg={8}>
            <PillarsOverview pillarsToStatuses={this.state.pillars.pillarsToStatuses}
                             grades={this.state.pillars.grades}/>
          </Col>
          <Col xs={4} sm={4} md={4} lg={4}>
            <ZeroTrustReportLegend/>
          </Col>
        </Row>
        <Row>
          <Col xs={12} sm={12} md={12} lg={12}>
            <h4>What am I seeing?</h4>
            <p>
              The <a href="https://www.forrester.com/report/The+Zero+Trust+eXtended+ZTX+Ecosystem/-/E-RES137210">Zero Trust eXtended framework</a> categorizes its <b>recommendations</b> into 7 <b>pillars</b>. Infection Monkey
              Zero Trust edition tests some of those recommendations. The <b>tests</b> that the monkey executes
              produce <b>findings</b>. The tests, recommendations and pillars are then granted a <b>status</b> in accordance
              with the tests results.
            </p>
          </Col>
        </Row>
      </Grid>
    </div>);
  }

  generateRecommendationsSection() {
    return (<div id="recommendations-overview">
      <h2>Recommendations</h2>
      <p>
        Analyze each zero trust recommendation by pillar, and see if you've followed through with it. See test results
        to understand how the monkey tested your adherence to that recommendation.
      </p>
      {
        Object.keys(this.state.recommendations).map((pillar) =>
          <SinglePillarRecommendationsStatus
            key={pillar}
            pillar={pillar}
            recommendationsStatus={this.state.recommendations[pillar]}
            pillarsToStatuses={this.state.pillars.pillarsToStatuses}/>
        )
      }
    </div>);
  }

  generateFindingsSection() {
    return (<div id="findings-overview">
      <h2>Findings</h2>
      <p>
        Deep-dive into the details of each test, and see the explicit events and exact timestamps in which things
        happened in your network. This will enable you to match up with your SOC logs and alerts and to gain deeper
        insight as to what exactly happened during this test.
      </p>
      <FindingsSection pillarsToStatuses={this.state.pillars.pillarsToStatuses} findings={this.state.findings}/>
    </div>);
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined" || typeof this.state.pillars === "undefined" || typeof this.state.recommendations === "undefined";
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
    this.authFetch('/api/report/zero_trust/recommendations')
      .then(res => res.json())
      .then(res => {
        this.setState({
          recommendations: res
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
}

export default ZeroTrustReportPageComponent;
