import React, {Fragment} from 'react';
import {Col} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from "../report-components/common/ReportHeader";
import ReportLoader from "../report-components/common/ReportLoader";
import MustRunMonkeyWarning from "../report-components/common/MustRunMonkeyWarning";
import PrintReportButton from "../report-components/common/PrintReportButton";
import {extractExecutionStatusFromServerResponse} from "../report-components/common/ExecutionStatus";
import SummarySection from "../report-components/zerotrust/SummarySection";
import FindingsSection from "../report-components/zerotrust/FindingsSection";
import RecommendationsSection from "../report-components/zerotrust/RecommendationsSection";

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
    const refreshInterval = setInterval(this.updatePageState, 8000);
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
        <SummarySection allMonkeysAreDead={this.state.allMonkeysAreDead} pillars={this.state.pillars}/>
        <RecommendationsSection recommendations={this.state.recommendations}
                                pillarsToStatuses={this.state.pillars.pillarsToStatuses}/>
        <FindingsSection pillarsToStatuses={this.state.pillars.pillarsToStatuses} findings={this.state.findings}/>
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

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined"
      || typeof this.state.pillars === "undefined"
      || typeof this.state.recommendations === "undefined";
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
