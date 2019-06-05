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
      report: {},
      graph: {nodes: [], edges: []},
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  componentDidMount() {
    this.updateMonkeysRunning().then(res => this.getReportFromServer(res));
    this.updateMapFromServer();
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    let content;
    if (Object.keys(this.state.report).length === 0) {
      if (this.state.runStarted) {
        content = (<h1>Generating Report...</h1>);
      } else {
        content =
          <p className="alert alert-warning">
            <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
            You have to run a monkey before generating a report!
          </p>;
      }
    } else {
      content = this.generateReportContent();
    }

    return (
      <Col xs={12} lg={10}>
        <h1 className="page-title no-print">4. Security Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done']),
          runStarted: res['completed_steps']['run_monkey']
        });
        return res;
      });
  };

  updateMapFromServer = () => {
    this.authFetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        res.edges.forEach(edge => {
          edge.color = {'color': edgeGroupToColor(edge.group)};
        });
        this.setState({graph: res});
        this.props.onStatusChange();
      });
  };

  getReportFromServer(res) {
    if (res['completed_steps']['run_monkey']) {
      this.authFetch('/api/report')
        .then(res => res.json())
        .then(res => {
          this.setState({
            report: res
          });
        });
    }
  }

  generateReportContent() {
    return (
      <div>
        <div className="text-center no-print" style={{marginBottom: '20px'}}>
          <Button bsSize="large" onClick={() => {
            print();
          }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
        </div>
        <div className="report-page">
          {this.generateReportHeader()}
          <hr/>
          {this.generateReportOverviewSection()}
          {this.generateReportFindingsSection()}
          {this.generateReportRecommendationsSection()}
          {this.generateReportGlanceSection()}
          {this.generateAttackSection()}
          {this.generateReportFooter()}
        </div>
        <div className="text-center no-print" style={{marginTop: '20px'}}>
          <Button bsSize="large" onClick={() => {
            print();
          }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
        </div>
      </div>
    );
  }

  generateReportHeader() {
    return (
      <div id="header" className="row justify-content-between">
        <Col xs={8}>
          <div>
            <h1 style={{marginTop: '0px', marginBottom: '5px', color: '#666666', fontFamily: 'Alegreya'}}>Security Report</h1>
            <h1 style={{marginTop: '0px', marginBottom: '0px', color: '#ffcc00', fontFamily: 'Alegreya'}}>Infection <b>Monkey</b></h1>
          </div>
        </Col>
        <Col xs={4}>
          <img src={monkeyLogoImage}
               style={{
                 float: 'right',
                 width: '80px'
               }}/>
        </Col>
      </div>
    );
  }

  generateReportOverviewSection() {
    return (
      <div id="overview">
        <h2>
          Overview
        </h2>
        {
          this.state.report.glance.exploited.length > 0 ?
            (<p className="alert alert-danger">
              <i className="glyphicon glyphicon-exclamation-sign" style={{'marginRight': '5px'}}/>
              Critical security issues were detected!
            </p>) :
            (<p className="alert alert-success">
              <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
              No critical security issues were detected.
            </p>)
        }
        {
          this.state.allMonkeysAreDead ?
            ''
            :
            (<p className="alert alert-warning">
              <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
              Some monkeys are still running. To get the best report it's best to wait for all of them to finish
              running.
            </p>)
        }
        {
          this.state.report.glance.exploited.length > 0 ?
            ''
            :
            <p className="alert alert-info">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              To improve the monkey's detection rates, try adding users and passwords and enable the "Local
              network
              scan" config value under <b>Basic - Network</b>.
            </p>
        }
        <p>
          The first monkey run was started on <span
          className="label label-info">{this.state.report.overview.monkey_start_time}</span>. After <span
          className="label label-info">{this.state.report.overview.monkey_duration}</span>, all monkeys finished
          propagation attempts.
        </p>
        <p>
          The monkey started propagating from the following machines where it was manually installed:
          <ul>
            {this.state.report.overview.manual_monkeys.map(x => <li>{x}</li>)}
          </ul>
        </p>
        <p>
          The monkeys were run with the following configuration:
        </p>
        {
          this.state.report.overview.config_users.length > 0 ?
            <p>
              Usernames used for brute-forcing:
              <ul>
                {this.state.report.overview.config_users.map(x => <li>{x}</li>)}
              </ul>
              Passwords used for brute-forcing:
              <ul>
                {this.state.report.overview.config_passwords.map(x => <li>{x.substr(0, 3) + '******'}</li>)}
              </ul>
            </p>
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
                    {this.state.report.overview.config_exploits.map(x => <li>{x}</li>)}
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
                {this.state.report.overview.config_ips.map(x => <li>{x}</li>)}
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
                During this simulated attack the Monkey uncovered  <span
                className="label label-warning">
                    {this.state.report.overview.issues.filter(function (x) {
                      return x === true;
                    }).length} threats</span>:
                <ul>
                  {this.state.report.overview.issues[this.Issue.STOLEN_SSH_KEYS] ?
                    <li>Stolen SSH keys are used to exploit other machines.</li> : null }
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
                      CVE-2017-5638</a>)</li> : null }
                  {this.state.report.overview.issues[this.Issue.WEBLOGIC] ?
                    <li>Oracle WebLogic servers are vulnerable to remote code execution. (<a
                      href="https://nvd.nist.gov/vuln/detail/CVE-2017-10271">
                      CVE-2017-10271</a>)</li> : null }
                  {this.state.report.overview.issues[this.Issue.HADOOP] ?
                    <li>Hadoop/Yarn servers are vulnerable to remote code execution.</li> : null }
                  {this.state.report.overview.issues[this.Issue.PTH_CRIT_SERVICES_ACCESS] ?
                    <li>Mimikatz found login credentials of a user who has admin access to a server defined as critical.</li>: null }
                  {this.state.report.overview.issues[this.Issue.MSSQL] ?
                  <li>MS-SQL servers are vulnerable to remote code execution via xp_cmdshell command.</li> : null }
                </ul>
              </div>
              :
              <div>
                During this simulated attack the Monkey uncovered <span
                className="label label-success">0 threats</span>.
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
                    <li>Weak segmentation - Machines from different segments are able to
                      communicate.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.TUNNEL] ?
                    <li>Weak segmentation - Machines were able to communicate over unused ports.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.SHARED_LOCAL_ADMIN] ?
                    <li>Shared local administrator account - Different machines have the same account as a local administrator.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.SHARED_PASSWORDS] ?
                    <li>Multiple users have the same password</li> : null}
                </ul>
              </div>
              :
              <div>
                The Monkey did not find any issues.
              </div>
          }
        </div>
        { this.state.report.overview.cross_segment_issues.length > 0 ?
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
                     <h3>Domain related recommendations</h3> : null }
        <div>
          {this.generateIssues(this.state.report.recommendations.domain_issues)}
        </div>
        {/* Checks if there are any issues. If there are more then one: render the title. Otherwise,
         * don't render it (since the issues themselves will be empty. */}
        {Object.keys(this.state.report.recommendations.issues).length !== 0 ?
          <h3>Machine related recommendations</h3> : null }
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
            className="label label-warning">{this.state.report.glance.scanned.length}</span> machines and
            successfully breached <span
            className="label label-danger">{this.state.report.glance.exploited.length}</span> of them.
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
          <span>Exploit <i className="fa fa-lg fa-minus" style={{color: '#cc0200'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Scan <i className="fa fa-lg fa-minus" style={{color: '#ff9900'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Tunnel <i className="fa fa-lg fa-minus" style={{color: '#0158aa'}}/></span>
          <b style={{color: '#aeaeae'}}> | </b>
          <span>Island Communication <i className="fa fa-lg fa-minus" style={{color: '#a9aaa9'}}/></span>
        </div>
        <div style={{position: 'relative', height: '80vh'}}>
          <ReactiveGraph graph={this.state.graph} options={options}/>
        </div>
        <div style={{marginBottom: '20px'}}>
          <BreachedServers data={this.state.report.glance.exploited}/>
        </div>
        <div style={{marginBottom: '20px'}}>
          <PostBreach data={this.state.report.glance.scanned}/>
        </div>
        <div style={{marginBottom: '20px'}}>
          <ScannedServers data={this.state.report.glance.scanned}/>
        </div>
        <div style={{position: 'relative', height: '80vh'}}>
        {this.generateReportPthMap()}
        </div>
        <div style={{marginBottom: '20px'}}>
          <StolenPasswords data={this.state.report.glance.stolen_creds.concat(this.state.report.glance.ssh_keys)}/>
        </div>
        <div>
          <StrongUsers data = {this.state.report.glance.strong_users} />
        </div>
      </div>
    );
  }

  generateReportPthMap() {
    return (
      <div id="pth">
        <h3>
          Credentials Map
        </h3>
        <p>
          This map visualizes possible attack paths through the network using credential compromise. Paths represent lateral movement opportunities by attackers.
        </p>
        <div className="map-legend">
          <b>Legend: </b>
          <span>Access credentials <i className="fa fa-lg fa-minus" style={{color: '#0158aa'}}/></span> <b style={{color: '#aeaeae'}}> | </b>
        </div>
        <div>
          <PassTheHashMapPageComponent graph={this.state.report.glance.pth_map} />
        </div>
        <br />
      </div>
    );
  }

  generateAttackSection() {
    return (<div id="attack">
              <h3>
                ATT&CK report
              </h3>
              <p>
                This report shows information about ATT&CK techniques used by Infection Monkey.
              </p>
              <div>
                <AttackReport/>
              </div>
              <br />
            </div>)
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
    return data_array.map(badge_data => <span className="label label-info" style={{margin: '2px'}}>{badge_data}</span>);
  }

  generateCrossSegmentIssue(crossSegmentIssue) {
    return <li>
      {'Communication possible from ' + crossSegmentIssue['source_subnet'] + ' to ' + crossSegmentIssue['target_subnet']}
        <CollapsibleWellComponent>
          <ul>
            {crossSegmentIssue['issues'].map(x =>
              x['is_self'] ?
                <li>
                  {'Machine ' + x['hostname'] + ' has both ips: ' + x['source'] + ' and ' + x['target']}
                </li>
                :
                <li>
                  {'IP ' + x['source'] + ' (' + x['hostname'] + ') connected to IP ' + x['target']
                  + ' using the services: ' + Object.keys(x['services']).join(', ')}
                </li>
            )}
          </ul>
        </CollapsibleWellComponent>
      </li>;
  }

  generateShellshockPathListBadges(paths) {
    return paths.map(path => <span className="label label-warning" style={{margin: '2px'}}>{path}</span>);
  }

  generateSmbPasswordIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">SMB</span> attack.
          <br/>
          The Monkey authenticated over the SMB protocol with user <span
          className="label label-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSmbPthIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">SMB</span> attack.
          <br/>
          The Monkey used a pass-the-hash attack over SMB protocol with user <span
          className="label label-success">{issue.username}</span>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateWmiPasswordIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">WMI</span> attack.
          <br/>
          The Monkey authenticated over the WMI protocol with user <span
          className="label label-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateWmiPthIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">WMI</span> attack.
          <br/>
          The Monkey used a pass-the-hash attack over WMI protocol with user <span
          className="label label-success">{issue.username}</span>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSshIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">SSH</span> attack.
          <br/>
          The Monkey authenticated over the SSH protocol with user <span
          className="label label-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSshKeysIssue(issue) {
    return (
        <li>
          Protect <span className="label label-success">{issue.ssh_key}</span> private key with a pass phrase.
          <CollapsibleWellComponent>
            The machine <span className="label label-primary">{issue.machine}</span> (<span
            className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
            className="label label-danger">SSH</span> attack.
            <br/>
            The Monkey authenticated over the SSH protocol with private key <span
            className="label label-success">{issue.ssh_key}</span>.
          </CollapsibleWellComponent>
        </li>
      );
  }

  generateRdpIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">RDP</span> attack.
          <br/>
          The Monkey authenticated over the RDP protocol with user <span
          className="label label-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSambaCryIssue(issue) {
    return (
      <li>
        Change <span className="label label-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <br/>
        Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">SambaCry</span> attack.
          <br/>
          The Monkey authenticated over the SMB protocol with user <span
          className="label label-success">{issue.username}</span> and its password, and used the SambaCry
          vulnerability.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateVsftpdBackdoorIssue(issue) {
    return (
      <li>
        Update your VSFTPD server to the latest version vsftpd-3.0.3.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) has a backdoor running at port  <span
          className="label label-danger">6200</span>.
          <br/>
          The attack was made possible because the VSFTPD server was not patched against CVE-2011-2523.
          <br/><br/>In July 2011, it was discovered that vsftpd version 2.3.4 downloadable from the master site had been compromised.
          Users logging into a compromised vsftpd-2.3.4 server may issue a ":)" smileyface as the username and gain a command shell on port 6200.
          <br/><br/>
          The Monkey executed commands by first logging in with ":)" in the username and then sending commands to the backdoor at port 6200.
          <br/><br/>Read more about the security issue and remediation <a
                      href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-2523"
                    >here</a>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateElasticIssue(issue) {
    return (
      <li>
        Update your Elastic Search server to version 1.4.3 and up.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to an <span
          className="label label-danger">Elastic Groovy</span> attack.
          <br/>
          The attack was made possible because the Elastic Search server was not patched against CVE-2015-1427.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateShellshockIssue(issue) {
    return (
      <li>
        Update your Bash to a ShellShock-patched version.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">ShellShock</span> attack.
          <br/>
          The attack was made possible because the HTTP server running on TCP port <span
          className="label label-info">{issue.port}</span> was vulnerable to a shell injection attack on the
          paths: {this.generateShellshockPathListBadges(issue.paths)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateAzureIssue(issue) {
    return (
      <li>
        Delete VM Access plugin configuration files.
        <CollapsibleWellComponent>
          Credentials could be stolen from <span
          className="label label-primary">{issue.machine}</span> for the following users <span
          className="label label-primary">{issue.users}</span>. Read more about the security issue and remediation <a
                      href="https://www.guardicore.com/2018/03/recovering-plaintext-passwords-azure/"
                    >here</a>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateConfickerIssue(issue) {
    return (
      <li>
        Install the latest Windows updates or upgrade to a newer operating system.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">Conficker</span> attack.
          <br/>
          The attack was made possible because the target machine used an outdated and unpatched operating system
          vulnerable to Conficker.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateIslandCrossSegmentIssue(issue) {
    return (
      <li>
        Segment your network and make sure there is no communication between machines from different segments.
        <CollapsibleWellComponent>
          The network can probably be segmented. A monkey instance on <span
          className="label label-primary">{issue.machine}</span> in the
          networks {this.generateInfoBadges(issue.networks)}
          could directly access the Monkey Island server in the
          networks {this.generateInfoBadges(issue.server_networks)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSharedCredsDomainIssue(issue) {
    return (
    <li>
        Some domain users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
           {this.generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSharedCredsIssue(issue) {
    return (
    <li>
        Some users are sharing passwords, this should be fixed by changing passwords.
        <CollapsibleWellComponent>
          These users are sharing access password:
           {this.generateInfoBadges(issue.shared_with)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateSharedLocalAdminsIssue(issue) {
    return (
    <li>
        Make sure the right administrator accounts are managing the right machines, and that there isn’t an unintentional local admin sharing.
        <CollapsibleWellComponent>
          Here is a list of machines which the account <span
          className="label label-primary">{issue.username}</span> is defined as an administrator:
          {this.generateInfoBadges(issue.shared_machines)}
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateStrongUsersOnCritIssue(issue) {
    return (
    <li>
        This critical machine is open to attacks via strong users with access to it.
        <CollapsibleWellComponent>
          The services: {this.generateInfoBadges(issue.services)} have been found on the machine
          thus classifying it as a critical machine.
          These users has access to it:
           {this.generateInfoBadges(issue.threatening_users)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateTunnelIssue(issue) {
    return (
      <li>
        Use micro-segmentation policies to disable communication other than the required.
        <CollapsibleWellComponent>
          Machines are not locked down at port level. Network tunnel was set up from <span
          className="label label-primary">{issue.machine}</span> to <span
          className="label label-primary">{issue.dest}</span>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateStruts2Issue(issue) {
    return (
      <li>
        Upgrade Struts2 to version 2.3.32 or 2.5.10.1 or any later versions.
        <CollapsibleWellComponent>
          Struts2 server at <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="label label-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible because the server is using an old version of Jakarta based file upload
          Multipart parser. For possible work-arounds and more info read <a
                      href="https://cwiki.apache.org/confluence/display/WW/S2-045"
                    >here</a>.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateWebLogicIssue(issue) {
    return (
      <li>
        Install Oracle <a href="http://www.oracle.com/technetwork/security-advisory/cpuoct2017-3236626.html">
        critical patch updates.</a> Or update to the latest version. Vulnerable versions are
        10.3.6.0.0, 12.1.3.0.0, 12.2.1.1.0 and 12.2.1.2.0.
        <CollapsibleWellComponent>
          Oracle WebLogic server at <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="label label-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible due to incorrect permission assignment in Oracle Fusion Middleware
          (subcomponent: WLS Security).
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateHadoopIssue(issue) {
    return (
      <li>
        Run Hadoop in secure mode (<a href="http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SecureMode.html">
        add Kerberos authentication</a>).
        <CollapsibleWellComponent>
          The Hadoop server at <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="label label-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible due to default Hadoop/Yarn configuration being insecure.
        </CollapsibleWellComponent>
      </li>
    );
  }

generateMSSQLIssue(issue) {
    return(
      <li>
        Disable the xp_cmdshell option.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> (<span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="label label-danger">MSSQL exploit attack</span>.
          <br/>
          The attack was made possible because the target machine used an outdated MSSQL server configuration allowing
          the usage of the xp_cmdshell command. To learn more about how to disable this feature, read <a
           href="https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option?view=sql-server-2017">
            Microsoft's documentation. </a>
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateIssue = (issue) => {
    let data;
    switch (issue.type) {
      case 'vsftp':
        data = this.generateVsftpdBackdoorIssue(issue);
        break;
      case 'smb_password':
        data = this.generateSmbPasswordIssue(issue);
        break;
      case 'smb_pth':
        data = this.generateSmbPthIssue(issue);
        break;
      case 'wmi_password':
        data = this.generateWmiPasswordIssue(issue);
        break;
      case 'wmi_pth':
        data = this.generateWmiPthIssue(issue);
        break;
      case 'ssh':
        data = this.generateSshIssue(issue);
        break;
      case 'ssh_key':
        data = this.generateSshKeysIssue(issue);
        break;
      case 'rdp':
        data = this.generateRdpIssue(issue);
        break;
      case 'sambacry':
        data = this.generateSambaCryIssue(issue);
        break;
      case 'elastic':
        data = this.generateElasticIssue(issue);
        break;
      case 'shellshock':
        data = this.generateShellshockIssue(issue);
        break;
      case 'conficker':
        data = this.generateConfickerIssue(issue);
        break;
      case 'island_cross_segment':
        data = this.generateIslandCrossSegmentIssue(issue);
        break;
      case 'shared_passwords':
        data = this.generateSharedCredsIssue(issue);
        break;
      case 'shared_passwords_domain':
        data = this.generateSharedCredsDomainIssue(issue);
        break;
      case 'shared_admins_domain':
        data = this.generateSharedLocalAdminsIssue(issue);
        break;
      case 'strong_users_on_crit':
        data = this.generateStrongUsersOnCritIssue(issue);
        break;
      case 'tunnel':
        data = this.generateTunnelIssue(issue);
        break;
      case 'azure_password':
        data = this.generateAzureIssue(issue);
        break;
      case 'struts2':
        data = this.generateStruts2Issue(issue);
        break;
      case 'weblogic':
        data = this.generateWebLogicIssue(issue);
        break;
      case 'hadoop':
        data = this.generateHadoopIssue(issue);
        break;
      case 'mssql':
        data = this.generateMSSQLIssue(issue);
        break;
    }
    return data;
  };

  generateIssues = (issues) => {
    let issuesDivArray = [];
    for (let machine of Object.keys(issues)) {
      issuesDivArray.push(
        <li>
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
