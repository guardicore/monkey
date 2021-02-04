import React, {Fragment} from 'react';
import BreachedServers from 'components/report-components/security/BreachedServers';
import ScannedServers from 'components/report-components/security/ScannedServers';
import PostBreach from 'components/report-components/security/PostBreach';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, getOptions} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/security/StolenPasswords';
import CollapsibleWellComponent from 'components/report-components/security/CollapsibleWell';
import {Line} from 'rc-progress';
import AuthComponent from '../AuthComponent';
import StrongUsers from 'components/report-components/security/StrongUsers';
import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';
import SecurityIssuesGlance from './common/SecurityIssuesGlance';
import PrintReportButton from './common/PrintReportButton';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMinus } from '@fortawesome/free-solid-svg-icons/faMinus';
import guardicoreLogoImage from '../../images/guardicore-logo.png'
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import '../../styles/App.css';


class ReportPageComponent extends AuthComponent {

  Issue =
    {
      WEAK_PASSWORD: 0,
      STOLEN_CREDS: 1,
      ELASTIC: 2,
      SAMBACRY: 3,
      SHELLSHOCK: 4,
      CONFICKER: 5,
      AZURE: 6,
      STOLEN_SSH_KEYS: 7,
      STRUTS2: 8,
      WEBLOGIC: 9,
      HADOOP: 10,
      PTH_CRIT_SERVICES_ACCESS: 11,
      MSSQL: 12,
      VSFTPD: 13
    };

  Warning =
    {
      CROSS_SEGMENT: 0,
      TUNNEL: 1,
      SHARED_LOCAL_ADMIN: 2,
      SHARED_PASSWORDS: 3,
      SHARED_PASSWORDS_DOMAIN: 4
    };

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
    this.authFetch('/api/netmap/nodeStates')
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
     this.setState({ report: this.props.report })
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
        <div className="report-page">
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
      <div id="overview">
        <h2>
          Overview
        </h2>
        <SecurityIssuesGlance issuesFound={this.state.report.glance.exploited.length > 0}/>
        {
          this.state.report.glance.exploited.length > 0 ?
            ''
            :
            <p className="alert alert-info">
              <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
              To improve the monkey's detection rates, try adding users and passwords and enable the "Local
              network
              scan" config value under <b>Basic - Network</b>.
            </p>
        }
        <p>
          The first monkey run was started on <span
          className="badge badge-info">{this.state.report.overview.monkey_start_time}</span>. After <span
          className="badge badge-info">{this.state.report.overview.monkey_duration}</span>, all monkeys finished
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
    return (
      <div id="findings">
        <h3>
          Security Findings
        </h3>
        <div>
          <h3>
            Immediate Threats
          </h3>
          {
            this.state.report.overview.issues.filter(function (x) {
              return x === true;
            }).length > 0 ?
              <div>
                During this simulated attack the Monkey uncovered <span
                className="badge badge-warning">
                    {this.state.report.overview.issues.filter(function (x) {
                      return x === true;
                    }).length} threats</span>:
                <ul>
                  {this.state.report.overview.issues[this.Issue.STOLEN_SSH_KEYS] ?
                    <li>Stolen SSH keys are used to exploit other machines.</li> : null}
                  {this.state.report.overview.issues[this.Issue.STOLEN_CREDS] ?
                    <li>Stolen credentials are used to exploit other machines.</li> : null}
                  {this.state.report.overview.issues[this.Issue.ELASTIC] ?
                    <li>Elasticsearch servers are vulnerable to <a
                      href="https://www.cvedetails.com/cve/cve-2015-1427">CVE-2015-1427</a>.
                    </li> : null}
                  {this.state.report.overview.issues[this.Issue.VSFTPD] ?
                    <li>VSFTPD is vulnerable to <a
                      href="https://www.rapid7.com/db/modules/exploit/unix/ftp/vsftpd_234_backdoor">CVE-2011-2523</a>.
                    </li> : null}
                  {this.state.report.overview.issues[this.Issue.SAMBACRY] ?
                    <li>Samba servers are vulnerable to ‘SambaCry’ (<a
                      href="https://www.samba.org/samba/security/CVE-2017-7494.html"
                    >CVE-2017-7494</a>).</li> : null}
                  {this.state.report.overview.issues[this.Issue.SHELLSHOCK] ?
                    <li>Machines are vulnerable to ‘Shellshock’ (<a
                      href="https://www.cvedetails.com/cve/CVE-2014-6271">CVE-2014-6271</a>).
                    </li> : null}
                  {this.state.report.overview.issues[this.Issue.CONFICKER] ?
                    <li>Machines are vulnerable to ‘Conficker’ (<a
                      href="https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2008/ms08-067"
                    >MS08-067</a>).</li> : null}
                  {this.state.report.overview.issues[this.Issue.WEAK_PASSWORD] ?
                    <li>Machines are accessible using passwords supplied by the user during the Monkey’s
                      configuration.</li> : null}
                  {this.state.report.overview.issues[this.Issue.AZURE] ?
                    <li>Azure machines expose plaintext passwords. (<a
                      href="https://www.guardicore.com/2018/03/recovering-plaintext-passwords-azure/"
                    >More info</a>)</li> : null}
                  {this.state.report.overview.issues[this.Issue.STRUTS2] ?
                    <li>Struts2 servers are vulnerable to remote code execution. (<a
                      href="https://cwiki.apache.org/confluence/display/WW/S2-045">
                      CVE-2017-5638</a>)</li> : null}
                  {this.state.report.overview.issues[this.Issue.WEBLOGIC] ?
                    <li>Oracle WebLogic servers are susceptible to a remote code execution vulnerability.</li> : null}
                  {this.state.report.overview.issues[this.Issue.HADOOP] ?
                    <li>Hadoop/Yarn servers are vulnerable to remote code execution.</li> : null}
                  {this.state.report.overview.issues[this.Issue.PTH_CRIT_SERVICES_ACCESS] ?
                    <li>Mimikatz found login credentials of a user who has admin access to a server defined as
                      critical.</li> : null}
                  {this.state.report.overview.issues[this.Issue.MSSQL] ?
                    <li>MS-SQL servers are vulnerable to remote code execution via xp_cmdshell command.</li> : null}
                </ul>
              </div>
              :
              <div>
                During this simulated attack the Monkey uncovered <span
                className="badge badge-success">0 threats</span>.
              </div>
          }
        </div>
        <div>
          <h3>
            Potential Security Issues
          </h3>
          {
            this.state.report.overview.warnings.filter(function (x) {
              return x === true;
            }).length > 0 ?
              <div>
                The Monkey uncovered the following possible set of issues:
                <ul>
                  {this.state.report.overview.warnings[this.Warning.CROSS_SEGMENT] ?
                    <li key={this.Warning.CROSS_SEGMENT}>Weak segmentation - Machines from different segments are able to
                      communicate.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.TUNNEL] ?
                    <li key={this.Warning.TUNNEL}>Weak segmentation - Machines were able to communicate over unused ports.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.SHARED_LOCAL_ADMIN] ?
                    <li key={this.Warning.SHARED_LOCAL_ADMIN}>Shared local administrator account - Different machines have the same account as a local
                      administrator.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.SHARED_PASSWORDS] ?
                    <li key={this.Warning.SHARED_PASSWORDS}>Multiple users have the same password</li> : null}
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
                {this.state.report.overview.cross_segment_issues.map(x => this.generateCrossSegmentIssue(x))}
              </ul>
            </div>
          </div>
          :
          ''
        }
      </div>
    );
  }

  generateReportRecommendationsSection() {
    return (
      <div id="recommendations">
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
      (100 * this.state.report.glance.exploited.length) / this.state.report.glance.scanned.length;
    return (
      <div id="glance">
        <h3>
          The Network from the Monkey's Eyes
        </h3>
        <div>
          <p>
            The Monkey discovered <span
            className="badge badge-warning">{this.state.report.glance.scanned.length}</span> machines and
            successfully breached <span
            className="badge badge-danger">{this.state.report.glance.exploited.length}</span> of them.
          </p>
          <div className="text-center" style={{margin: '10px'}}>
            <Line style={{width: '300px', marginRight: '5px'}} percent={exploitPercentage} strokeWidth="4"
                  trailWidth="4"
                  strokeColor="#d9534f" trailColor="#f0ad4e"/>
            <b>{Math.round(exploitPercentage)}% of scanned machines exploited</b>
          </div>
        </div>
        <p>
          From the attacker's point of view, the network looks like this:
        </p>
        <div className="map-legend">
          <b>Legend: </b>
          <span>Exploit <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#cc0200'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Scan <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#ff9900'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Tunnel <FontAwesomeIcon icon={faMinus} size="lg" style={{color: '#0158aa'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Island Communication <FontAwesomeIcon icon={faMinus} size="lg"  style={{color: '#a9aaa9'}}/></span>
        </div>
        <div style={{position: 'relative', height: '80vh'}}>
          <ReactiveGraph graph={this.state.graph} options={getOptions(this.state.nodeStateList)}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <ScannedServers data={this.state.report.glance.scanned}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <BreachedServers data={this.state.report.glance.exploited}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <PostBreach data={this.state.report.glance.scanned}/>
        </div>

        <div style={{marginBottom: '20px'}}>
          <StolenPasswords data={this.state.report.glance.stolen_creds.concat(this.state.report.glance.ssh_keys)}/>
        </div>
        <div>
          <StrongUsers data={this.state.report.glance.strong_users}/>
        </div>
      </div>
    );
  }

  generateReportFooter() {
    return (
      <div id="footer" className="text-center" style={{marginTop: '20px'}}>
        For questions, suggestions or any other feedback
        contact: <a href="mailto://labs@guardicore.com" className="no-print">labs@guardicore.com</a>
        <div className="force-print" style={{display: 'none'}}>labs@guardicore.com</div>
        <img src={guardicoreLogoImage} alt="GuardiCore" className="center-block" style={{height: '50px'}}/>
      </div>
    );
  }

  generateInfoBadges(data_array) {
    return data_array.map(badge_data => <span key={badge_data} className="badge badge-info" style={{margin: '2px'}}>{badge_data}</span>);
  }

  generateCrossSegmentIssue(crossSegmentIssue) {
    let crossSegmentIssueOverview = 'Communication possible from '
      + `${crossSegmentIssue['source_subnet']} to ${crossSegmentIssue['target_subnet']}`;

    return (
      <li key={crossSegmentIssueOverview}>
        {crossSegmentIssueOverview}
        <CollapsibleWellComponent>
          <ul className='cross-segment-issues'>
            {crossSegmentIssue['issues'].map(
              issue => this.generateCrossSegmentIssueListItem(issue)
            )}
          </ul>
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateCrossSegmentIssueListItem(issue) {
    if (issue['is_self']) {
      return this.generateCrossSegmentSingleHostMessage(issue);
    }

    return this.generateCrossSegmentMultiHostMessage(issue);
  }

  generateCrossSegmentSingleHostMessage(issue) {
    return (
      <li key={issue['hostname']}>
        {`Machine ${issue['hostname']} has both ips: ${issue['source']} and ${issue['target']}`}
      </li>
    );
  }

  generateCrossSegmentMultiHostMessage(issue) {
    return (
      <li key={issue['source'] + issue['target']}>
        IP {issue['source']} ({issue['hostname']}) was able to communicate with
        IP {issue['target']} using:
        <ul>
          {issue['icmp'] && <li key='icmp'>ICMP</li>}
          {this.generateCrossSegmentServiceListItems(issue)}
        </ul>
      </li>
    );
  }

  generateCrossSegmentServiceListItems(issue) {
    let service_list_items = [];

    for (const [service, info] of Object.entries(issue['services'])) {
      service_list_items.push(
        <li key={service}>
          <span className='cross-segment-service'>{service}</span> ({info['display_name']})
        </li>
      );
    }

    return service_list_items;
  }

  generateShellshockPathListBadges(paths) {
    return paths.map(path => <span className="badge badge-warning" style={{margin: '2px'}} key={path}>{path}</span>);
  }

  generateSmbPasswordIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SMB</span> attack.
          <br/>
          The Monkey authenticated over the SMB protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSmbPthIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SMB</span> attack.
          <br/>
          The Monkey used a pass-the-hash attack over SMB protocol with user <span
          className="badge badge-success">{issue.username}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateWmiPasswordIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">WMI</span> attack.
          <br/>
          The Monkey authenticated over the WMI protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateWmiPthIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">WMI</span> attack.
          <br/>
          The Monkey used a pass-the-hash attack over WMI protocol with user <span
          className="badge badge-success">{issue.username}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSshIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SSH</span> attack.
          <br/>
          The Monkey authenticated over the SSH protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSshKeysIssue(issue) {
    return (
      <>
        Protect <span className="badge badge-success">{issue.ssh_key}</span> private key with a pass phrase.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SSH</span> attack.
          <br/>
          The Monkey authenticated over the SSH protocol with private key <span
          className="badge badge-success">{issue.ssh_key}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }


  generateSambaCryIssue(issue) {
    return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <br/>
        Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SambaCry</span> attack.
          <br/>
          The Monkey authenticated over the SMB protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password, and used the SambaCry
          vulnerability.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateVsftpdBackdoorIssue(issue) {
    return (
      <>
        Update your VSFTPD server to the latest version vsftpd-3.0.3.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) has a backdoor running at port <span
          className="badge badge-danger">6200</span>.
          <br/>
          The attack was made possible because the VSFTPD server was not patched against CVE-2011-2523.
          <br/><br/>In July 2011, it was discovered that vsftpd version 2.3.4 downloadable from the master site had been
          compromised.
          Users logging into a compromised vsftpd-2.3.4 server may issue a ":)" smileyface as the username and gain a command
          shell on port 6200.
          <br/><br/>
          The Monkey executed commands by first logging in with ":)" in the username and then sending commands to the backdoor
          at port 6200.
          <br/><br/>Read more about the security issue and remediation <a
          href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-2523"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateElasticIssue(issue) {
    return (
      <>
        Update your Elastic Search server to version 1.4.3 and up.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to an <span
          className="badge badge-danger">Elastic Groovy</span> attack.
          <br/>
          The attack was made possible because the Elastic Search server was not patched against CVE-2015-1427.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateShellshockIssue(issue) {
    return (
      <>
        Update your Bash to a ShellShock-patched version.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">ShellShock</span> attack.
          <br/>
          The attack was made possible because the HTTP server running on TCP port <span
          className="badge badge-info">{issue.port}</span> was vulnerable to a shell injection attack on the
          paths: {this.generateShellshockPathListBadges(issue.paths)}.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateAzureIssue(issue) {
    return (
      <>
        Delete VM Access plugin configuration files.
        <CollapsibleWellComponent>
          Credentials could be stolen from <span
          className="badge badge-primary">{issue.machine}</span> for the following users <span
          className="badge badge-primary">{issue.users}</span>. Read more about the security issue and remediation <a
          href="https://www.guardicore.com/2018/03/recovering-plaintext-passwords-azure/"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateConfickerIssue(issue) {
    return (
      <>
        Install the latest Windows updates or upgrade to a newer operating system.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">Conficker</span> attack.
          <br/>
          The attack was made possible because the target machine used an outdated and unpatched operating system
          vulnerable to Conficker.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateIslandCrossSegmentIssue(issue) {
    return (
      <>
        Segment your network and make sure there is no communication between machines from different segments.
        <CollapsibleWellComponent>
          The network can probably be segmented. A monkey instance on <span
          className="badge badge-primary">{issue.machine}</span> in the
          networks {this.generateInfoBadges(issue.networks)}
          could directly access the Monkey Island server in the
          networks {this.generateInfoBadges(issue.server_networks)}.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSharedCredsDomainIssue(issue) {
    return (
      <>
        Some domain users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
          {this.generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSharedCredsIssue(issue) {
    return (
      <>
        Some users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
          {this.generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateSharedLocalAdminsIssue(issue) {
    return (
      <>
        Make sure the right administrator accounts are managing the right machines, and that there isn’t an unintentional local
        admin sharing.
        <CollapsibleWellComponent>
          Here is a list of machines which the account <span
          className="badge badge-primary">{issue.username}</span> is defined as an administrator:
          {this.generateInfoBadges(issue.shared_machines)}
        </CollapsibleWellComponent>
      </>
    );
  }

  generateStrongUsersOnCritIssue(issue) {
    return (
      <>
        This critical machine is open to attacks via strong users with access to it.
        <CollapsibleWellComponent>
          The services: {this.generateInfoBadges(issue.services)} have been found on the machine
          thus classifying it as a critical machine.
          These users has access to it:
          {this.generateInfoBadges(issue.threatening_users)}.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateTunnelIssue(issue) {
    return (
      <>
        Use micro-segmentation policies to disable communication other than the required.
        <CollapsibleWellComponent>
          Machines are not locked down at port level. Network tunnel was set up from <span
          className="badge badge-primary">{issue.machine}</span> to <span
          className="badge badge-primary">{issue.dest}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateStruts2Issue(issue) {
    return (
      <>
        Upgrade Struts2 to version 2.3.32 or 2.5.10.1 or any later versions.
        <CollapsibleWellComponent>
          Struts2 server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible because the server is using an old version of Jakarta based file upload
          Multipart parser. For possible work-arounds and more info read <a
          href="https://cwiki.apache.org/confluence/display/WW/S2-045"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateDrupalIssue(issue) {
    return (
      <>
        Upgrade Drupal server to versions 8.5.11, 8.6.10, or later.
        <CollapsibleWellComponent>
          Drupal server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote command execution</span> attack.
          <br/>
          The attack was made possible because the server is using an old version of Drupal, for which REST API is
          enabled. For possible workarounds, fixes and more info read
          <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-6340">here</a>.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateWebLogicIssue(issue) {
    return (
      <>
        Update Oracle WebLogic server to the latest supported version.
        <CollapsibleWellComponent>
          Oracle WebLogic server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to one of <span
          className="badge badge-danger">remote code execution</span> attacks.
          <br/>
          The attack was made possible due to one of the following vulnerabilities:
          <a href={'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-10271'}> CVE-2017-10271</a> or
          <a href={'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-2725'}> CVE-2019-2725</a>
        </CollapsibleWellComponent>
      </>
    );
  }

  generateHadoopIssue(issue) {
    return (
      <>
        Run Hadoop in secure mode (<a
        href="http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SecureMode.html">
        add Kerberos authentication</a>).
        <CollapsibleWellComponent>
          The Hadoop server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible due to default Hadoop/Yarn configuration being insecure.
        </CollapsibleWellComponent>
      </>
    );
  }

  generateMSSQLIssue(issue) {
    return (
      <>
        Disable the xp_cmdshell option.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">MSSQL exploit attack</span>.
          <br/>
          The attack was made possible because the target machine used an outdated MSSQL server configuration allowing
          the usage of the xp_cmdshell command. To learn more about how to disable this feature, read <a
          href="https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option?view=sql-server-2017">
          Microsoft's documentation. </a>
        </CollapsibleWellComponent>
      </>
    );
  }

  generateIssue = (issue) => {
    let issueData;
    switch (issue.type) {
      case 'vsftp':
        issueData = this.generateVsftpdBackdoorIssue(issue);
        break;
      case 'smb_password':
        issueData = this.generateSmbPasswordIssue(issue);
        break;
      case 'smb_pth':
        issueData = this.generateSmbPthIssue(issue);
        break;
      case 'wmi_password':
        issueData = this.generateWmiPasswordIssue(issue);
        break;
      case 'wmi_pth':
        issueData = this.generateWmiPthIssue(issue);
        break;
      case 'ssh':
        issueData = this.generateSshIssue(issue);
        break;
      case 'ssh_key':
        issueData = this.generateSshKeysIssue(issue);
        break;
      case 'sambacry':
        issueData = this.generateSambaCryIssue(issue);
        break;
      case 'elastic':
        issueData = this.generateElasticIssue(issue);
        break;
      case 'shellshock':
        issueData = this.generateShellshockIssue(issue);
        break;
      case 'conficker':
        issueData = this.generateConfickerIssue(issue);
        break;
      case 'island_cross_segment':
        issueData = this.generateIslandCrossSegmentIssue(issue);
        break;
      case 'shared_passwords':
        issueData = this.generateSharedCredsIssue(issue);
        break;
      case 'shared_passwords_domain':
        issueData = this.generateSharedCredsDomainIssue(issue);
        break;
      case 'shared_admins_domain':
        issueData = this.generateSharedLocalAdminsIssue(issue);
        break;
      case 'strong_users_on_crit':
        issueData = this.generateStrongUsersOnCritIssue(issue);
        break;
      case 'tunnel':
        issueData = this.generateTunnelIssue(issue);
        break;
      case 'azure_password':
        issueData = this.generateAzureIssue(issue);
        break;
      case 'struts2':
        issueData = this.generateStruts2Issue(issue);
        break;
      case 'weblogic':
        issueData = this.generateWebLogicIssue(issue);
        break;
      case 'hadoop':
        issueData = this.generateHadoopIssue(issue);
        break;
      case 'mssql':
        issueData = this.generateMSSQLIssue(issue);
        break;
      case 'drupal':
        issueData = this.generateDrupalIssue(issue);
        break;
    }
    return <li key={JSON.stringify(issue)}>{issueData}</li>;
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
