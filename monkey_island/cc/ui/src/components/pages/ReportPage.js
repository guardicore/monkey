import React from 'react';
import {Button, Col} from 'react-bootstrap';
import BreachedServers from 'components/report-components/BreachedServers';
import ScannedServers from 'components/report-components/ScannedServers';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/StolenPasswords';
import CollapsibleWellComponent from 'components/report-components/CollapsibleWell';
import {Line} from 'rc-progress';

class ReportPageComponent extends React.Component {

  Issue =
    {
      WEAK_PASSWORD: 0,
      STOLEN_CREDS: 1,
      ELASTIC: 2,
      SAMBACRY: 3,
      SHELLSHOCK: 4,
      CONFICKER: 5
    };

  Warning =
    {
      CROSS_SEGMENT: 0,
      TUNNEL: 1
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
    this.interval = setInterval(this.updateMapFromServer, 1000);
  }

  updateMonkeysRunning = () => {
    return fetch('/api')
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

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  updateMapFromServer = () => {
    fetch('/api/netmap')
      .then(res => res.json())
      .then(res => {
        res.edges.forEach(edge => {
          edge.color = edgeGroupToColor(edge.group);
        });
        this.setState({graph: res});
        this.props.onStatusChange();
      });
  };

  getReportFromServer(res) {
    if (res['completed_steps']['run_monkey']) {
      fetch('/api/report')
        .then(res => res.json())
        .then(res => {
          this.setState({
            report: res
          });
        });
    }
  }

  generateInfoBadges(data_array) {
    return data_array.map(badge_data => <span className="label label-info" style={{margin: '2px'}}>{badge_data}</span>);
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">SMB</span> attack.
          <br/>
          The attack succeeded by authenticating over SMB protocol with user <span
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">SMB</span> attack.
          <br/>
          The attack succeeded by using a pass-the-hash attack over SMB protocol with user <span
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">WMI</span> attack.
          <br/>
          The attack succeeded by authenticating over WMI protocol with user <span
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">WMI</span> attack.
          <br/>
          The attack succeeded by using a pass-the-hash attack over WMI protocol with user <span
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">SSH</span> attack.
          <br/>
          The attack succeeded by authenticating over SSH protocol with user <span
          className="label label-success">{issue.username}</span> and its password.
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">RDP</span> attack.
          <br/>
          The attack succeeded by authenticating over RDP protocol with user <span
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
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">SambaCry</span> attack.
          <br/>
          The attack succeeded by authenticating over SMB protocol with user <span
          className="label label-success">{issue.username}</span> and its password, and by using the SambaCry
          vulnerability.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateElasticIssue(issue) {
    return (
      <li>
        Update your Elastic Search server to version 1.4.3 and up.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to an <span
          className="label label-danger">Elastic Groovy</span> attack.
          <br/>
          The attack succeeded because the Elastic Search server was not parched against CVE-2015-1427.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateShellshockIssue(issue) {
    return (
      <li>
        Update your Bash to a ShellShock-patched version.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">ShellShock</span> attack.
          <br/>
          The attack succeeded because the HTTP server running on port <span
          className="label label-info">{issue.port}</span> was vulnerable to a shell injection attack on the
          paths: {this.generateShellshockPathListBadges(issue.paths)}.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateConfickerIssue(issue) {
    return (
      <li>
        Install the latest Windows updates or upgrade to a newer operating system.
        <CollapsibleWellComponent>
          The machine <span className="label label-primary">{issue.machine}</span> with the following address <span
          className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span
          className="label label-danger">Conficker</span> attack.
          <br/>
          The attack succeeded because the target machine uses an outdated and unpatched operating system vulnerable to
          Conficker.
        </CollapsibleWellComponent>
      </li>
    );
  }

  generateCrossSegmentIssue(issue) {
    return (
      <li>
        Segment your network. Make sure machines can't access machines from other segments.
        <CollapsibleWellComponent>
          The network can probably be segmented. A monkey instance on <span
          className="label label-primary">{issue.machine}</span> in the
          networks {this.generateInfoBadges(issue.networks)}
          could directly access the Monkey Island C&C server in the
          networks {this.generateInfoBadges(issue.server_networks)}.
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

  generateIssue = (issue) => {
    let data;
    switch (issue.type) {
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
      case 'cross_segment':
        data = this.generateCrossSegmentIssue(issue);
        break;
      case 'tunnel':
        data = this.generateTunnelIssue(issue);
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

  didMonkeyFindIssues = () => {
    for (let issue of Object.keys(this.state.report.overview.issues)) {
      if (this.state.report.overview.issues[issue]) {
        return true;
      }
    }
    return false;
  };


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
      let exploitPercentage =
        (100 * this.state.report.glance.exploited.length) / this.state.report.glance.scanned.length;
      content =
        (
          <div>
            <div className="text-center no-print" style={{marginBottom: '20px'}}>
              <Button bsSize="large" onClick={() => {
                print();
              }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
            </div>
            <div className="report-page">
              <div id="overview">
                <h1>
                  Overview
                </h1>
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
                      Users to try:
                      <ul>
                        {this.state.report.overview.config_users.map(x => <li>{x}</li>)}
                      </ul>
                      Passwords to try:
                      <ul>
                        {this.state.report.overview.config_passwords.map(x => <li>{x.substr(0, 3) + '******'}</li>)}
                      </ul>
                    </p>
                    :
                    <p>
                      No Users and Passwords were provided for the monkey.
                    </p>
                }
                {
                  this.state.report.overview.config_exploits.length > 0 ?
                    (
                      this.state.report.overview.config_exploits[0] === 'default' ?
                        ''
                        :
                        <p>
                          Used the following exploit methods:
                          <ul>
                            {this.state.report.overview.config_exploits.map(x => <li>{x}</li>)}
                          </ul>
                        </p>
                    )
                    :
                    <p>
                      Don't use any exploit.
                    </p>
                }
                {
                  this.state.report.overview.config_ips.length > 0 ?
                    <p>
                      Scan the following IPs:
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
                      Monkeys were configured to avoid scanning of the local network.
                    </p>
                }
                <p>
                  A full report of the Monkeys activities follows.
                </p>
              </div>
              <div id="findings">
                <h1>
                  Security Findings
                </h1>
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
                        className="label label-warning">
                    {this.state.report.overview.issues.filter(function (x) {
                      return x === true;
                    }).length} issues</span>:
                        <ul>
                          {this.state.report.overview.issues[this.Issue.WEAK_PASSWORD] ?
                            <li>Users with passwords supplied in config.</li> : null}
                          {this.state.report.overview.issues[this.Issue.STOLEN_CREDS] ?
                            <li>Stolen credentials were used to exploit other machines.</li> : null}
                          {this.state.report.overview.issues[this.Issue.ELASTIC] ?
                            <li>Elastic Search servers not patched for <a
                              href="https://www.cvedetails.com/cve/cve-2015-1427">CVE-2015-1427</a>.
                            </li> : null}
                          {this.state.report.overview.issues[this.Issue.SAMBACRY] ?
                            <li>Samba servers not patched for ‘SambaCry’ (<a
                              href="https://www.samba.org/samba/security/CVE-2017-7494.html"
                            >CVE-2017-7494</a>).</li> : null}
                          {this.state.report.overview.issues[this.Issue.SHELLSHOCK] ?
                            <li>Machines not patched for the ‘Shellshock’ (<a
                              href="https://www.cvedetails.com/cve/CVE-2014-6271">CVE-2014-6271</a>).
                            </li> : null}
                          {this.state.report.overview.issues[this.Issue.CONFICKER] ?
                            <li>Machines not patched for the ‘Conficker’ (<a
                              href="https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2008/ms08-067"
                            >MS08-067</a>).</li> : null}
                        </ul>
                      </div>
                      :
                      <div>
                        During this simulated attack the Monkey uncovered <span
                        className="label label-success">0 issues</span>.
                      </div>
                  }
                </div>
                <div>
                  <h3>
                    Security Issues
                  </h3>
                  {
                    this.state.report.overview.warnings.filter(function (x) {
                      return x === true;
                    }).length > 0 ?
                      <div>
                        The monkey uncovered the following possible set of issues:
                        <ul>
                          {this.state.report.overview.warnings[this.Warning.CROSS_SEGMENT] ?
                            <li>Possible cross segment traffic. Infected machines could communicate with the
                              Monkey Island despite crossing segment boundaries using unused ports.</li> : null}
                          {this.state.report.overview.warnings[this.Warning.TUNNEL] ?
                            <li>Lack of Micro-segmentation, machines successfully tunneled monkey activity
                              using unused ports.</li> : null}
                        </ul>
                      </div>
                      :
                      <div>
                        The monkey did not find any issues.
                      </div>
                  }
                </div>
              </div>
              <div id="recommendations">
                <h1>
                  Recommendations
                </h1>
                <div>
                  {this.generateIssues(this.state.report.recommendations.issues)}
                </div>
              </div>
              <div id="glance">
                <h1>
                  The Network from the Monkey's Eyes
                </h1>
                <div>
                  <p>
                    The Monkey discovered <span
                    className="label label-warning">{this.state.report.glance.scanned.length}</span> machines and
                    successfully breached <span
                    className="label label-danger">{this.state.report.glance.exploited.length}</span> of them.
                    <br/>
                    In addition, while attempting to exploit additional hosts , security software installed in the
                    network should have picked up the attack attempts and logged them.
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
                  <span>Exploit <i className="fa fa-lg fa-minus" style={{color: '#cc0200'}} /></span>
                  <b style={{color: '#aeaeae'}}> | </b>
                  <span>Scan <i className="fa fa-lg fa-minus" style={{color: '#ff9900'}} /></span>
                  <b style={{color: '#aeaeae'}}> | </b>
                  <span>Tunnel <i className="fa fa-lg fa-minus" style={{color: '#0158aa'}} /></span>
                  <b style={{color: '#aeaeae'}}> | </b>
                  <span>Island Communication <i className="fa fa-lg fa-minus" style={{color: '#a9aaa9'}} /></span>
                </div>
                <div style={{position: 'relative', height: '80vh'}}>
                  <ReactiveGraph graph={this.state.graph} options={options}/>
                </div>
                <div style={{marginBottom: '20px'}}>
                  <BreachedServers data={this.state.report.glance.exploited}/>
                </div>
                <div style={{marginBottom: '20px'}}>
                  <ScannedServers data={this.state.report.glance.scanned}/>
                </div>
                <div>
                  <StolenPasswords data={this.state.report.glance.stolen_creds}/>
                </div>
              </div>
            </div>
            <div className="text-center no-print" style={{marginTop: '20px'}}>
              <Button bsSize="large" onClick={() => {
                print();
              }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
            </div>
          </div>
        );
    }

    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">4. Security Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }
}

export default ReportPageComponent;
