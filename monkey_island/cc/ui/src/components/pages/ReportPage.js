import React from 'react';
import {Col} from 'react-bootstrap';
import BreachedServers from 'components/report-components/BreachedServers';
import ScannedServers from 'components/report-components/ScannedServers';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {options, edgeGroupToColor} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/StolenPasswords';
import ScannedBreachedChart from 'components/report-components/ScannedBreachedChart';

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
      graph: {nodes: [], edges: []}
    };
  }

  componentDidMount() {
    this.getReportFromServer();
    this.updateMapFromServer();
    this.interval = setInterval(this.updateMapFromServer, 1000);
  }

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

  getReportFromServer() {
    fetch('/api/report')
      .then(res => res.json())
      .then(res => {
        this.setState({
          report: res
        });
      });
  }

  generateInfoBadges(data_array) {
    return data_array.map(badge_data => <span className="label label-info" style={{margin: '2px'}}>{badge_data}</span>);
  }

  generateShellshockPathListBadges(paths) {
    return paths.map(path =>  <span className="label label-warning" style={{margin: '2px'}}>{path}</span>);
  }

  generateSmbPasswordIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">SMB</span> attack.
        <br />
        The attack succeeded by authenticating over SMB protocol with user <span className="label label-success">{issue.username}</span> and its password.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateSmbPthIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">SMB</span> attack.
        <br />
        The attack succeeded by using a pass-the-hash attack over SMB protocol with user <span className="label label-success">{issue.username}</span>.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateWmiPasswordIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">WMI</span> attack.
        <br />
        The attack succeeded by authenticating over WMI protocol with user <span className="label label-success">{issue.username}</span> and its password.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateWmiPthIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">WMI</span> attack.
        <br />
        The attack succeeded by using a pass-the-hash attack over WMI protocol with user <span className="label label-success">{issue.username}</span>.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateSshIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">SSH</span> attack.
        <br />
        The attack succeeded by authenticating over SSH protocol with user <span className="label label-success">{issue.username}</span> and its password.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateRdpIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">RDP</span> attack.
        <br />
        The attack succeeded by authenticating over RDP protocol with user <span className="label label-success">{issue.username}</span> and its password.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateSambaCryIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">SambaCry</span> attack.
        <br />
        The attack succeeded by authenticating over SMB protocol with user <span className="label label-success">{issue.username}</span> and its password, and by using the SambaCry vulnerability.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up.</li>
          <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
        </ul>
      </div>
    );
  }

  generateElasticIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to an <span className="label label-danger">Elastic Groovy</span> attack.
        <br />
        The attack succeeded because the Elastic Search server was not parched against CVE-2015-1427.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Update your Elastic Search server to version 1.4.3 and up.</li>
        </ul>
      </div>
    );
  }

  generateShellshockIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following IP address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">ShellShock</span> attack.
        <br />
        The attack succeeded because the HTTP server running on port <span className="label label-info">{issue.port}</span> was vulnerable to a shell injection attack on the paths: {this.generateShellshockPathListBadges(issue.paths)}.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Update your Bash to a ShellShock-patched version.</li>
        </ul>
      </div>
    );
  }

  generateConfickerIssue(issue) {
    return (
      <div>
        The machine <span className="label label-primary">{issue.machine}</span> with the following address <span className="label label-info" style={{margin: '2px'}}>{issue.ip_address}</span> was vulnerable to a <span className="label label-danger">Conficker</span> attack.
        <br />
        The attack succeeded because the target machine uses an outdated and unpatched operating system vulnerable to Conficker.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Install the latest Windows updates or upgrade to a newer operating system.</li>
        </ul>
      </div>
    );
  }

  generateCrossSegmentIssue(issue) {
    return (
      <div>
        The network can probably be segmented. A monkey instance on <span className="label label-primary">{issue.machine}</span> in the networks {this.generateInfoBadges(issue.networks)} could directly access the Monkey Island C&C server in the networks {this.generateInfoBadges(issue.server_networks)}.
        <br />
        In order to protect the network, the following steps should be performed:
        <ul className="report">
          <li className="report">Segment your network. Make sure machines can't access machines from other segments.</li>
        </ul>
      </div>
    );
  }

  generateTunnelIssue(issue) {
    return (
      <div>
        Machines are not locked down at port level. Network tunnel was set up from <span className="label label-primary">{issue.machine}</span> to <span className="label label-primary">{issue.dest}</span>.
        <br />
        In order to protect the machine, the following steps should be performed:
        <ul className="report">
          <li className="report">Use micro-segmentation policies to disable communication other than the required.</li>
        </ul>
      </div>
    );
  }

  generateIssue = (issue, index) => {
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
    return (
      <div>
        <h4><b><i>Issue #{index+1}</i></b></h4>
        {data}
      </div>
    );
  };

  render() {
    let content;
    if (Object.keys(this.state.report).length === 0) {
      content = (<h1>Generating Report...</h1>);
    } else {
      content =
        (
          <div>
            <div id="overview">
              <h1>
                Overview
              </h1>
              <p>
                The first monkey run was started on <span className="label label-info">{this.state.report.overview.monkey_start_time}</span>. After <span className="label label-info">{this.state.report.overview.monkey_duration}</span>, all monkeys finished propagation attempts.
              </p>
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
                During this simulated attack the Monkey uncovered <span className="label label-warning">{this.state.report.overview.issues.filter(function(x){return x===true;}).length} issues</span>, detailed below. The security issues uncovered include:
                <ul className="report">
                  {this.state.report.overview.issues[this.Issue.WEAK_PASSWORD] ? <li className="report">Users with weak passwords.</li> : null}
                  {this.state.report.overview.issues[this.Issue.STOLEN_CREDS] ?<li className="report">Stolen passwords/hashes were used to exploit other machines.</li> : null}
                  {this.state.report.overview.issues[this.Issue.ELASTIC] ? <li className="report">Elastic Search servers not patched for <a href="https://www.cvedetails.com/cve/cve-2015-1427" className="report">CVE-2015-1427</a>.</li> : null}
                  {this.state.report.overview.issues[this.Issue.SAMBACRY] ? <li className="report">Samba servers not patched for ‘SambaCry’ (<a href="https://www.samba.org/samba/security/CVE-2017-7494.html" className="report">CVE-2017-7494</a>).</li> : null}
                  {this.state.report.overview.issues[this.Issue.SHELLSHOCK] ? <li className="report">Machines not patched for the ‘Shellshock’ (<a href="https://www.cvedetails.com/cve/CVE-2014-6271" className="report">CVE-2014-6271</a>).</li> : null}
                  {this.state.report.overview.issues[this.Issue.CONFICKER] ? <li className="report">Machines not patched for the ‘Conficker’ (<a href="https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2008/ms08-067" className="report">MS08-067</a>).</li> : null}
                </ul>
              </div>
              <div>
                <h3>
                  Security Issues
                </h3>
                The monkey uncovered the following possible set of issues:
                <ul className="report">
                  {this.state.report.overview.warnings[this.Warning.CROSS_SEGMENT] ? <li className="report">Possible cross segment traffic. Infected machines could communicate with the Monkey Island despite crossing segment boundaries using unused ports.</li> : null}
                  {this.state.report.overview.warnings[this.Warning.TUNNEL] ? <li className="report">Lack of port level segmentation, machines successfully tunneled monkey activity using unused ports.</li> : null}
                </ul>
              </div>
            </div>
            <div id="recommendations">
              <h1>
                Recommendations
              </h1>
                <div>
                  {this.state.report.recommendations.issues.map(this.generateIssue)}
                </div>
            </div>
            <div id="glance">
              <h1>
                The Network from the Monkey's Eyes
              </h1>
              <div>
                <Col lg={10}>
                  <p>
                    The Monkey discovered <span className="label label-info">{this.state.report.glance.scanned.length}</span> machines and successfully breached <span className="label label-warning">{this.state.report.glance.exploited.length}</span> of them.
                    <br />
                    In addition, while attempting to exploit additional hosts , security software installed in the network should have picked up the attack attempts and logged them.
                    <br />
                    Detailed recommendations in the <a href="#recommendations">next part of the report</a>.
                  </p>
                </Col>
                <Col lg={2}>
                  <div style={{marginBottom: '20px'}}>
                    <ScannedBreachedChart scanned={this.state.report.glance.scanned.length} exploited={this.state.report.glance.exploited.length} />
                  </div>
                </Col>
              </div>
              <p>
                From the attacker's point of view, the network looks like this:
              </p>
              <div style={{height: '80vh'}}>
                <ReactiveGraph graph={this.state.graph} options={options} />
              </div>
              <div style={{marginBottom: '20px'}}>
                <BreachedServers data={this.state.report.glance.exploited} />
              </div>
              <div style={{marginBottom: '20px'}}>
                <ScannedServers data={this.state.report.glance.scanned} />
              </div>
              <div>
                <StolenPasswords data={this.state.report.glance.stolen_creds} />
              </div>
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
