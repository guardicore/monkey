import React from 'react';
import {Route} from 'react-router-dom';
import {Col, Nav} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import MustRunMonkeyWarning from '../report-components/common/MustRunMonkeyWarning';
import AttackReport from '../report-components/AttackReport'
import SecurityReport from '../report-components/SecurityReport'
import ZeroTrustReport from '../report-components/ZeroTrustReport'
import {extractExecutionStatusFromServerResponse} from '../report-components/common/ExecutionStatus';
import MonkeysStillAliveWarning from '../report-components/common/MonkeysStillAliveWarning';


class ReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.sectionsOrder = ['security', 'zeroTrust', 'attack'];
    this.state = {
      securityReport: {},
      attackReport: {},
      zeroTrustReport: {},
      allMonkeysAreDead: false,
      runStarted: true,
      selectedSection: ReportPageComponent.selectReport(this.sectionsOrder),
      sections: [{key: 'security', title: 'Security report'},
        {key: 'zeroTrust', title: 'Zero trust report'},
        {key: 'attack', title: 'ATT&CK report'}]
    };
  }

  static selectReport(reports) {
    let url = window.location.href;
    for (let report_name in reports) {
      if (Object.prototype.hasOwnProperty.call(reports, report_name) && url.endsWith(reports[report_name])) {
        return reports[report_name];
      }
    }
  }

  getReportFromServer(res) {
    if (res['completed_steps']['run_monkey']) {
      this.authFetch('/api/report/security')
        .then(res => res.json())
        .then(res => {
          this.setState({
            securityReport: res
          });
        });
      this.authFetch('/api/attack/report')
        .then(res => res.json())
        .then(res => {
          this.setState({
            attackReport: res
          });
        });
      this.getZeroTrustReportFromServer().then((ztReport) => {
        this.setState({zeroTrustReport: ztReport})
      });
    }
  }

  getZeroTrustReportFromServer = async () => {
    let ztReport = {findings: {}, principles: {}, pillars: {}};
    await this.authFetch('/api/report/zero_trust/findings')
      .then(res => res.json())
      .then(res => {
        ztReport.findings = res;
      });
    await this.authFetch('/api/report/zero_trust/principles')
      .then(res => res.json())
      .then(res => {
        ztReport.principles = res;
      });
    await this.authFetch('/api/report/zero_trust/pillars')
      .then(res => res.json())
      .then(res => {
        ztReport.pillars = res;
      });
    return ztReport
  };

  componentWillUnmount() {
    clearInterval(this.state.ztReportRefreshInterval);
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        this.setState(extractExecutionStatusFromServerResponse(res));
        return res;
      });
  };

  componentDidMount() {
    const ztReportRefreshInterval = setInterval(this.updateZeroTrustReportFromServer, 8000);
    this.setState({ztReportRefreshInterval: ztReportRefreshInterval});
    this.updateMonkeysRunning().then(res => this.getReportFromServer(res));
  }

  setSelectedSection = (key) => {
    this.setState({
      selectedSection: key
    });
  };

  renderNav = () => {
    return (
      <Route render={({history}) => (
        <Nav variant='tabs'
             fill
             activeKey={this.state.selectedSection}
             onSelect={(key) => {
               this.setSelectedSection(key);
               history.push(key)
             }}
             className={'report-nav'}>
          {this.state.sections.map(section => this.renderNavButton(section))}
        </Nav>)}/>)
  };

  renderNavButton = (section) => {
    return (
      <Nav.Item key={section.key}>
        <Nav.Link key={section.key}
                  eventKey={section.key}
                  onSelect={() => {
                  }}>
          {section.title}
        </Nav.Link>
      </Nav.Item>)
  };

  getReportContent() {
    switch (this.state.selectedSection) {
      case 'security':
        return (<SecurityReport report={this.state.securityReport}/>);
      case 'attack':
        return (<AttackReport report={this.state.attackReport}/>);
      case 'zeroTrust':
        return (<ZeroTrustReport report={this.state.zeroTrustReport}/>);
    }
  }

  render() {
    let content;

    if (this.state.runStarted) {
      content = this.getReportContent();
    } else {
      content = <MustRunMonkeyWarning/>;
    }
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 10}}
           className={'report-wrapper'}>
        <h1 className='page-title no-print'>3. Security Reports</h1>
        {this.renderNav()}
        <MonkeysStillAliveWarning allMonkeysAreDead={this.state.allMonkeysAreDead}/>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }
}

export default ReportPageComponent;
