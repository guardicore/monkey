import React, {Fragment} from 'react';
import Pluralize from 'pluralize';
import BreachedServers from 'components/report-components/security/BreachedServers';
import ScannedServers from 'components/report-components/security/ScannedServers';
import PostBreach from 'components/report-components/security/PostBreach';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, getOptions} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/security/StolenPasswords';
import {Line} from 'rc-progress';
import AuthComponent from '../AuthComponent';
import StrongUsers from 'components/report-components/security/StrongUsers';
import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';
import SecurityIssuesGlance from './common/SecurityIssuesGlance';
import PrintReportButton from './common/PrintReportButton';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faMinus} from '@fortawesome/free-solid-svg-icons/faMinus';
import guardicoreLogoImage from '../../images/guardicore-logo.png'
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import '../../styles/App.css';
import {smbPasswordReport, smbPthReport} from './security/issues/SmbIssue';
import {hadoopIssueOverview, hadoopIssueReport} from './security/issues/HadoopIssue';
import {mssqlIssueOverview, mssqlIssueReport} from './security/issues/MssqlIssue';
import {wmiPasswordIssueReport, wmiPthIssueReport} from './security/issues/WmiIssue';
import {sshKeysReport, shhIssueReport, sshIssueOverview} from './security/issues/SshIssue';
import {log4shellIssueOverview, log4shellIssueReport} from './security/issues/Log4ShellIssue';
import {
  crossSegmentIssueOverview,
  crossSegmentIssueReport,
  islandCrossSegmentIssueReport
} from './security/issues/CrossSegmentIssue';
import {
  sharedCredsDomainIssueReport, sharedCredsIssueReport, sharedLocalAdminsIssueReport,
  sharedAdminsDomainIssueOverview,
  sharedPasswordsIssueOverview
} from './security/issues/SharedPasswordsIssue';
import {tunnelIssueReport, tunnelIssueOverview} from './security/issues/TunnelIssue';
import {stolenCredsIssueOverview} from './security/issues/StolenCredsIssue';
import {weakPasswordIssueOverview} from './security/issues/WeakPasswordIssue';
import {strongUsersOnCritIssueReport} from './security/issues/StrongUsersOnCritIssue';
import {
  zerologonIssueOverview,
  zerologonIssueReport,
  zerologonOverviewWithFailedPassResetWarning
} from './security/issues/ZerologonIssue';
import {powershellIssueOverview, powershellIssueReport} from './security/issues/PowershellIssue';


class ReportPageComponent extends AuthComponent {

  credentialTypes = {
    PASSWORD: 'password',
    HASH: 'hash',
    KEY: 'key'
  }

  issueContentTypes = {
    OVERVIEW: 'overview',
    REPORT: 'report',
    TYPE: 'type'
  }

  issueTypes = {
    WARNING: 'warning',
    DANGER: 'danger'
  }

  IssueDescriptorEnum =
    {
      'SmbExploiter': {
        [this.issueContentTypes.REPORT]: {
          [this.credentialTypes.PASSWORD]: smbPasswordReport,
          [this.credentialTypes.HASH]: smbPthReport
        },
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'HadoopExploiter': {
        [this.issueContentTypes.OVERVIEW]: hadoopIssueOverview,
        [this.issueContentTypes.REPORT]: hadoopIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'MSSQLExploiter': {
        [this.issueContentTypes.OVERVIEW]: mssqlIssueOverview,
        [this.issueContentTypes.REPORT]: mssqlIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'WmiExploiter': {
        [this.issueContentTypes.REPORT]: {
          [this.credentialTypes.PASSWORD]: wmiPasswordIssueReport,
          [this.credentialTypes.HASH]: wmiPthIssueReport
        },
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'SSHExploiter': {
        [this.issueContentTypes.OVERVIEW]: sshIssueOverview,
        [this.issueContentTypes.REPORT]: {
          [this.credentialTypes.PASSWORD]: shhIssueReport,
          [this.credentialTypes.KEY]: sshKeysReport
        },
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'PowerShellExploiter': {
        [this.issueContentTypes.OVERVIEW]: powershellIssueOverview,
        [this.issueContentTypes.REPORT]: powershellIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'ZerologonExploiter': {
        [this.issueContentTypes.OVERVIEW]: zerologonIssueOverview,
        [this.issueContentTypes.REPORT]: zerologonIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'Log4ShellExploiter': {
        [this.issueContentTypes.OVERVIEW]: log4shellIssueOverview,
        [this.issueContentTypes.REPORT]: log4shellIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'zerologon_pass_restore_failed': {
        [this.issueContentTypes.OVERVIEW]: zerologonOverviewWithFailedPassResetWarning
      },
      'island_cross_segment': {
        [this.issueContentTypes.OVERVIEW]: crossSegmentIssueOverview,
        [this.issueContentTypes.REPORT]: islandCrossSegmentIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.WARNING
      },
      'tunnel': {
        [this.issueContentTypes.OVERVIEW]: tunnelIssueOverview,
        [this.issueContentTypes.REPORT]: tunnelIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.WARNING
      },
      'shared_passwords': {
        [this.issueContentTypes.OVERVIEW]: sharedPasswordsIssueOverview,
        [this.issueContentTypes.REPORT]: sharedCredsIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.WARNING
      },
      'shared_admins_domain': {
        [this.issueContentTypes.OVERVIEW]: sharedAdminsDomainIssueOverview,
        [this.issueContentTypes.REPORT]: sharedLocalAdminsIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.WARNING
      },
      'shared_passwords_domain': {
        [this.issueContentTypes.REPORT]: sharedCredsDomainIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.WARNING
      },
      'strong_users_on_crit': {
        [this.issueContentTypes.REPORT]: strongUsersOnCritIssueReport,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'weak_password': {
        [this.issueContentTypes.OVERVIEW]: weakPasswordIssueOverview,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      },
      'stolen_creds': {
        [this.issueContentTypes.OVERVIEW]: stolenCredsIssueOverview,
        [this.issueContentTypes.TYPE]: this.issueTypes.DANGER
      }
    }

  constructor(props) {
    super(props);
    this.state = {
      report: props.report,
      graph: {nodes: [], edges: []},
      nodeStateList: []
    };
  }

  componentDidMount() {
    this.getNodeStateListFromServer();
    this.updateMapFromServer();
  }

  getNodeStateListFromServer = () => {
    this.authFetch('/api/netmap/node-states')
      .then(res => res.json())
      .then(res => {
        this.setState({nodeStateList: res.node_states});
      });
  };

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  componentDidUpdate(prevProps) {
    if (this.props.report !== prevProps.report) {
      this.setState({report: this.props.report})
    }
  }

  render() {
    let content;

    if (this.stillLoadingDataFromServer()) {
      content = <ReportLoader loading={true}/>;
    } else {
      content =
        <div>
          {this.generateReportOverviewSection()}
          {this.generateReportFindingsSection()}
          {this.generateReportRecommendationsSection()}
          {this.generateReportGlanceSection()}
          {this.generateReportFooter()}
        </div>;
    }

    return (
      <Fragment>
        <div style={{marginBottom: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
        <div className='report-page'>
          <ReportHeader report_type={ReportTypes.security}/>
          <hr/>
          {content}
        </div>
        <div style={{marginTop: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
      </Fragment>
    );
  }

  stillLoadingDataFromServer() {
    return Object.keys(this.state.report).length === 0;
  }

  updateMapFromServer = () => {
    this.authFetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        res.edges.forEach(edge => {
          edge.color = {'color': edgeGroupToColor(edge.group)};
        });
        this.setState({graph: res});
      });
  };


  generateReportOverviewSection() {
    return (
      <div id='overview'>
        <h2>
          Overview
        </h2>
        <SecurityIssuesGlance issuesFound={this.state.report.glance.exploited_cnt > 0}/>
        {
          this.state.report.glance.exploited_cnt > 0 ?
            ''
            :
            <p className='alert alert-info'>
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              To improve the monkey's detection rates, try adding users and passwords and enable the "Local
              network scan" config value under <b>Basic - Network</b>.
            </p>
        }
        <p>
          The first monkey run was started on <span
          className='badge badge-info'>{this.state.report.overview.monkey_start_time}</span>. After <span
          className='badge badge-info'>{this.state.report.overview.monkey_duration}</span>, all monkeys finished
          propagation attempts.
        </p>
        <p>
          The monkey started propagating from the following machines where it was manually installed:
        </p>
        <ul>
          {this.state.report.overview.manual_monkeys.map(x => <li key={x}>{x}</li>)}
        </ul>
        <p>
          The monkeys were run with the following configuration:
        </p>
        {
          this.state.report.overview.config_users.length > 0 ?
            <>
              <p>
                Usernames used for brute-forcing:
              </p>
              <ul>
                {this.state.report.overview.config_users.map(x => <li key={x}>{x}</li>)}
              </ul>
              <p>
                Passwords used for brute-forcing:
              </p>
              <ul>
                {this.state.report.overview.config_passwords.map(x => <li key={x}>{x.substr(0, 3) + '******'}</li>)}
              </ul>
            </>
            :
            <p>
              Brute forcing uses stolen credentials only. No credentials were supplied during Monkey’s
              configuration.
            </p>
        }
        {
          this.state.report.overview.config_exploits.length > 0 ?
            (
              this.state.report.overview.config_exploits[0] === 'default' ?
                ''
                :
                <p>
                  The Monkey uses the following exploit methods:
                  <ul>
                    {this.state.report.overview.config_exploits.map(x => <li key={x}>{x}</li>)}
                  </ul>
                </p>
            )
            :
            <p>
              No exploits are used by the Monkey.
            </p>
        }
        {
          this.state.report.overview.config_ips.length > 0 ?
            <p>
              The Monkey scans the following IPs:
              <ul>
                {this.state.report.overview.config_ips.map(x => <li key={x}>{x}</li>)}
              </ul>
            </p>
            :
            ''
        }
        {
          this.state.report.overview.config_scan ?
            ''
            :
            <p>
              Note: Monkeys were configured to avoid scanning of the local network.
            </p>
        }
      </div>
    );
  }

  generateReportFindingsSection() {
    let overviews = this.getPotentialSecurityIssuesOverviews()
    return (
      <div id='findings'>
        <h3>
          Security Findings
        </h3>
        {this.getImmediateThreats()}
        <div>
          <h3>
            Potential Security Issues
          </h3>
          {
            overviews.length > 0 ?
              <div>
                The Monkey uncovered the following possible set of issues:
                <ul>
                  {this.getPotentialSecurityIssuesOverviews()}
                </ul>
              </div>
              :
              <div>
                The Monkey did not find any issues.
              </div>
          }
        </div>
        {this.state.report.overview.cross_segment_issues.length > 0 ?
          <div>
            <h3>
              Segmentation Issues
            </h3>
            <div>
              The Monkey uncovered the following set of segmentation issues:
              <ul>
                {this.state.report.overview.cross_segment_issues.map(x => crossSegmentIssueReport(x))}
              </ul>
            </div>
          </div>
          :
          ''
        }
      </div>
    );
  }

  getPotentialSecurityIssuesOverviews() {
    let overviews = [];
    let issues = this.state.report.overview.issues;

    for(let i=0; i < issues.length; i++) {
      if (this.isIssuePotentialSecurityIssue(issues[i])) {
        overviews.push(this.getIssueOverview(this.IssueDescriptorEnum[issues[i]]));
      }
    }
    return overviews;
  }

  isIssuePotentialSecurityIssue(issueName) {
    let issueDescriptor = this.IssueDescriptorEnum[issueName];
    return Object.prototype.hasOwnProperty.call(issueDescriptor, this.issueContentTypes.TYPE) &&
      issueDescriptor[this.issueContentTypes.TYPE] === this.issueTypes.WARNING &&
      Object.prototype.hasOwnProperty.call(issueDescriptor, this.issueContentTypes.OVERVIEW);
  }

  getImmediateThreats() {
    let threatCount = this.getImmediateThreatCount()
    return (
      <div>
        <h3>
          Immediate Threats
        </h3>
        <div>During this simulated attack the Monkey uncovered
          {
            <>
             <span className="badge badge-warning">
               {threatCount} threats
             </span>:
             <ul>
              {this.getImmediateThreatsOverviews()}
            </ul>
            </>
          }
        </div>
      </div>)
  }

  getImmediateThreatCount() {
    let threatCount = 0;
    let issues = this.state.report.overview.issues;

    for(let i=0; i < issues.length; i++) {
      if(this.isIssueImmediateThreat(issues[i])) {
        threatCount++;
      }
    }
    return threatCount;
  }

  isIssueImmediateThreat(issueName) {
    let issueDescriptor = this.IssueDescriptorEnum[issueName];
    return Object.prototype.hasOwnProperty.call(issueDescriptor, this.issueContentTypes.TYPE) &&
      issueDescriptor[this.issueContentTypes.TYPE] === this.issueTypes.DANGER &&
      Object.prototype.hasOwnProperty.call(issueDescriptor, this.issueContentTypes.OVERVIEW);
  }

  getImmediateThreatsOverviews() {
    let overviews = [];
    let issues = this.state.report.overview.issues;

    for(let i=0; i < issues.length; i++) {
      if (this.isIssueImmediateThreat(issues[i])) {
        if (issues[i] === 'ZerologonExploiter' && issues.includes('zerologon_pass_restore_failed')){
          overviews.push(this.getIssueOverview(this.IssueDescriptorEnum['zerologon_pass_restore_failed']));
        } else {
          overviews.push(this.getIssueOverview(this.IssueDescriptorEnum[issues[i]]));
        }
      }
    }
    return overviews;
  }

  getIssueOverview(issueDescriptor) {
    return issueDescriptor[this.issueContentTypes.OVERVIEW]();
  }

  generateReportRecommendationsSection() {
    return (
      <div id='recommendations'>
        {/* Checks if there are any domain issues. If there are more then one: render the title. Otherwise,
         * don't render it (since the issues themselves will be empty. */}
        {Object.keys(this.state.report.recommendations.domain_issues).length !== 0 ?
          <h3>Domain related recommendations</h3> : null}
        <div>
          {this.generateIssues(this.state.report.recommendations.domain_issues)}
        </div>
        {/* Checks if there are any issues. If there are more then one: render the title. Otherwise,
         * don't render it (since the issues themselves will be empty. */}
        {Object.keys(this.state.report.recommendations.issues).length !== 0 ?
          <h3>Machine related recommendations</h3> : null}
        <div>
          {this.generateIssues(this.state.report.recommendations.issues)}
        </div>
      </div>
    );
  }

  generateReportGlanceSection() {
    let exploitPercentage =
      (100 * this.state.report.glance.exploited_cnt) / this.state.report.glance.scanned.length;
    return (
      <div id='glance'>
        <h3>
          The Network from the Monkey's Eyes
        </h3>
        <div>
          <p>
            The Monkey discovered <span
            className='badge badge-warning'>{this.state.report.glance.scanned.length}</span> machines and
            successfully breached <span
            className='badge badge-danger'>{this.state.report.glance.exploited_cnt}</span> of them.
          </p>
          <div className='text-center' style={{margin: '10px'}}>
            <Line style={{width: '300px', marginRight: '5px'}} percent={exploitPercentage} strokeWidth='4'
                  trailWidth='4'
                  strokeColor='#d9534f' trailColor='#f0ad4e'/>
            <b>{Math.round(exploitPercentage)}% of scanned machines exploited</b>
          </div>
        </div>
        <p>
          From the attacker's point of view, the network looks like this:
        </p>
        <div className='map-legend'>
          <b>Legend: </b>
          <span>Exploit <FontAwesomeIcon icon={faMinus} size='lg' style={{color: '#cc0200'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Scan <FontAwesomeIcon icon={faMinus} size='lg' style={{color: '#ff9900'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Tunnel <FontAwesomeIcon icon={faMinus} size='lg' style={{color: '#0158aa'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Island Communication <FontAwesomeIcon icon={faMinus} size='lg' style={{color: '#a9aaa9'}}/></span>
        </div>
        <div style={{position: 'relative', height: '80vh'}}>
          <ReactiveGraph graph={this.state.graph} options={getOptions(this.state.nodeStateList)}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <ScannedServers data={this.state.report.glance.scanned}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <p>
            The Monkey successfully breached&nbsp;
            <span className="badge badge-danger">
              {this.state.report.glance.exploited_cnt}
            </span> {Pluralize('machine', this.state.report.glance.exploited_cnt)}:
          </p>
          <BreachedServers />
        </div>

        <div style={{marginBottom: '20px'}}>
          <PostBreach data={this.state.report.glance.scanned}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <StolenPasswords data={this.state.report.glance.stolen_creds}/>
        </div>
        <div>
          <StrongUsers data={this.state.report.glance.strong_users}/>
        </div>
      </div>
    );
  }

  generateReportFooter() {
    return (
      <div id='footer' className='text-center' style={{marginTop: '20px'}}>
        For questions, suggestions or any other feedback
        contact: <a href='mailto://labs@guardicore.com' className='no-print'>labs@guardicore.com</a>
        <div className='force-print' style={{display: 'none'}}>labs@guardicore.com</div>
        <img src={guardicoreLogoImage} alt='GuardiCore' className='center-block' style={{height: '50px'}}/>
      </div>
    );
  }

  generateIssue = (issue) => {
    let issueDescriptor = this.IssueDescriptorEnum[issue.type];

    let reportFnc = {};
    if (Object.prototype.hasOwnProperty.call(issue, 'credential_type') && issue.credential_type !== null) {
      reportFnc = issueDescriptor[this.issueContentTypes.REPORT][issue.credential_type];
    } else {
      reportFnc = issueDescriptor[this.issueContentTypes.REPORT];
    }
    let reportContents = reportFnc(issue);
    return <li key={JSON.stringify(issue)}>{reportContents}</li>;
  };

  generateIssues = (issues) => {
    let issuesDivArray = [];
    for (let machine of Object.keys(issues)) {
      issuesDivArray.push(
        <li key={JSON.stringify(machine)}>
          <h4><b>{machine}</b></h4>
          <ol>
            {issues[machine].map(this.generateIssue)}
          </ol>
        </li>
      );
    }
    return <ul>{issuesDivArray}</ul>;
  };
}

export default ReportPageComponent;
