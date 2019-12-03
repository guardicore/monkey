import '../../styles/report/ReportPage.scss';

import React from 'react';
import {Route} from 'react-router-dom';
import {Col, Nav, NavItem} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
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

  static selectReport(reports){
    let url = window.location.href;
    for (let report_name in reports){
      if (reports.hasOwnProperty(report_name) && url.endsWith(reports[report_name])){
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
      this.updateZeroTrustReportFromServer();
    }
  }

  updateZeroTrustReportFromServer = async () => {
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
      }).then(() => {
        this.setState({zeroTrustReport: ztReport})
      })
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
      <Nav bsStyle='tabs' justified
                 activeKey={this.state.selectedSection}
                 onSelect={(key) => {this.setSelectedSection(key); history.push(key)}}
                 className={'report-nav'}>
      {this.state.sections.map(section => this.renderNavButton(section))}
      </Nav>)}/>)
  };

  renderNavButton = (section) => {
    return (
        <NavItem key={section.key}
                 eventKey={section.key}
                 onSelect={() => {}}>
          {section.title}
        </NavItem>)};

  getReportContent() {
    switch(this.state.selectedSection){
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
      <Col xs={12} lg={12}>
        <h1 className='page-title no-print'>4. Security Reports</h1>
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
