import React, {useEffect, useState} from 'react';
import {Col, Nav} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import MustRunMonkeyWarning from '../report-components/common/MustRunMonkeyWarning';
import SecurityReport from '../report-components/SecurityReport';
import RansomwareReport from '../report-components/RansomwareReport';
import MonkeysStillAliveWarning from '../report-components/common/MonkeysStillAliveWarning';
import {doesAnyAgentExist, didAllAgentsShutdown} from '../utils/ServerUtils'
import {useNavigate} from 'react-router-dom';


function ReportPage() {
  const sections = ['security', 'ransomware'];
  const [securityReport, setSecurityReport] = useState({});
  const [ransomwareReport, setRansomwareReport] = useState({});
  const [allMonkeysAreDead, setAllMonkeysAreDead] = useState(false);
  const [runStarted, setRunStarted] = useState(true);
  const [selectedSection, setSelectedSection] = useState(selectReport(sections));
  const orderedSections = [{key: 'security', title: 'Security report'}, {key: 'ransomware', title: 'Ransomware report'}];
  const authComponent = new AuthComponent({});

  function selectReport(reports) {
    let url = window.location.href;
    for (let report_name in reports) {
      if (Object.prototype.hasOwnProperty.call(reports, report_name) && url.endsWith(reports[report_name])) {
        return reports[report_name];
      }
    }
  }

  function getReportFromServer() {
    doesAnyAgentExist(true).then(anyAgentExists => {
      if (anyAgentExists) {
          authComponent.authFetch('/api/report/security', {}, true)
          .then(res => res.json())
          .then(res => {
            setSecurityReport(res);
          });
          authComponent.authFetch('/api/report/ransomware', {}, true)
          .then(res => res.json())
          .then(res => {
            setRansomwareReport(res);
          });
      }
    });
  }

  function updateMonkeysRunning() {
    doesAnyAgentExist(true).then(anyAgentExists => {
      setRunStarted(anyAgentExists);
    });
    didAllAgentsShutdown(true).then(allAgentsShutdown => {
      setAllMonkeysAreDead(!runStarted || allAgentsShutdown);
    });
  }

  useEffect(() => {
    updateMonkeysRunning();
    getReportFromServer();
  }, [runStarted, allMonkeysAreDead]);

  function renderNav() {
    let navigate = useNavigate();
    return (
        <Nav variant='tabs'
             fill
             activeKey={selectedSection}
             onSelect={(key) => {
               setSelectedSection(key);
               navigate('/report/' + key);
             }}
             className={'report-nav'}>
          {orderedSections.map(section => renderNavButton(section))}
        </Nav>)
  }

  function renderNavButton(section) {
    return (
      <Nav.Item key={section.key}>
        <Nav.Link key={section.key}
                  eventKey={section.key}
                  onSelect={() => {
                  }}>
          {section.title}
        </Nav.Link>
      </Nav.Item>)
  }

  function getReportContent() {
    switch (selectedSection) {
      case 'security':
        return (<SecurityReport report={securityReport}/>);
      case 'ransomware':
        return (<RansomwareReport report={ransomwareReport}/>);
    }
  }

  function renderContent() {
    let content = <MustRunMonkeyWarning/>;

    if (runStarted) {
      content = getReportContent();
    }
    return content;
  }

  return (
    <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
          lg={{offset: 3, span: 9}} xl={{offset: 2, span: 10}}
          className={'main report-wrapper'}>
      <h1 className='page-title no-print'>3. Security Reports</h1>
      {renderNav()}
      <MonkeysStillAliveWarning allMonkeysAreDead={allMonkeysAreDead}/>
      <div style={{'fontSize': '1.2em'}}>
        {renderContent()}
      </div>
    </Col>
  );
}

export default ReportPage;
