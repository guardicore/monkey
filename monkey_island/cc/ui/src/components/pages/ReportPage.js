import React from 'react';
import {Col} from 'react-bootstrap';
import BreachedServers from 'components/report-components/BreachedServers';
import ScannedServers from 'components/report-components/ScannedServers';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {options, edgeGroupToColor} from 'components/map/MapOptions';
import StolenPasswords from 'components/report-components/StolenPasswords';
import ScannedBreachedChart from 'components/report-components/ScannedBreachedChart';

class ReportPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.stolen_passwords =
      [
        {username: 'admin', password: 'secretpassword', type: 'password', origin: 'Monkey-SMB'},
        {username: 'user', password: 'my_password', type: 'password', origin: 'Monkey-SMB2'},
        {username: 'dan', password: '066DDFD4EF0E9CD7C256FE77191EF43C', type: 'NTLM', origin: 'Monkey-RDP'},
        {username: 'joe', password: 'FDA95FBECA288D44AAD3B435B51404EE', type: 'LM', origin: 'Monkey-RDP'}
      ];
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
                {/* TODO: Replace 01/02/2017 21:45, 23:12 with data */}
                The monkey run was started on <span className="label label-info">01/02/2017 21:45</span>. After <span className="label label-info">23:12 minutes</span>, all monkeys finished propagation attempts.
              </p>
              <p>
                From the attacker's point of view, the network looks like this:
              </p>
              <div style={{height: '80vh'}}>
                <ReactiveGraph graph={this.state.graph} options={options} />
              </div>
              <div>
                {/* TODO: Replace 3 with data */}
                During this simulated attack the Monkey uncovered <span className="label label-warning">6 issues</span>, detailed below. The security issues uncovered included:
                <ul className="report">
                  {/* TODO: Replace lis with data */}
                  <li className="report">Weak user/passwords combinations.</li>
                  <li className="report">Stolen passwords/hashes used to exploit other machines.</li>
                  <li className="report">Elastic Search servers not patched for CVE-2015-1427 bug.</li>
                  <li className="report">Samba servers not patched for ‘SambaCry’ bug.</li>
                  <li className="report">Machines not patched for the ‘Shellshock’ bug.</li>
                  <li className="report">Machines not patched for the ‘Conficker’ bug.</li>
                </ul>
              </div>
              <div>
                In addition, the monkey uncovered the following possible set of issues:
                <ul className="report">
                  {/* TODO: Replace lis with data */}
                  <li className="report">Machines freely accessed the Monkey Island despite being on different networks.</li>
                  <li className="report">Machines are not locked down at port level, tunnels between network segments were setup successfully.</li>
                </ul>
              </div>
              <p>
                A full report of the Monkeys activities follows.
              </p>
            </div>
            <div id="glance">
              <h1>
                At a Glance
              </h1>
              <div>
                <Col lg={10}>
                  <p>
                    {/* TODO: Replace 6,2 with data */}
                    During the current run, the Monkey discovered <span className="label label-info">6</span> machines and successfully breached <span className="label label-warning">2</span> of them.
                    <br />
                    In addition, it attempted to exploit the rest, any security software installed in the network should have picked up the attack attempts and logged them.
                    <br />
                    Detailed recommendations in the <a href="#recommendations">next part of the report</a>.
                  </p>
                </Col>
                <Col lg={2}>
                  <div style={{marginBottom: '20px'}}>
                    <ScannedBreachedChart />
                  </div>
                </Col>
              </div>
              <div style={{marginBottom: '20px'}}>
                <BreachedServers data={this.state.report.exploited} />
              </div>
              <div style={{marginBottom: '20px'}}>
                <ScannedServers data={this.state.report.scanned} />
                {/* TODO: Add table of scanned servers */}
              </div>
              <div>
                <StolenPasswords data={this.stolen_passwords} />
              </div>
            </div>
            <div id="recommendations">
              <h1>
                Recommendations
              </h1>
              <div>
                <div>
                  <h4><b><i>Issue #1</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-SMB</span> with the following IP addresses <span className="label label-info">192.168.0.1</span> <span className="label label-info">10.0.0.18</span> was vulnerable to a <span className="label label-danger">SMB</span> attack.
                    <br />
                    The attack succeeded by authenticating over SMB protocol with user <span className="label label-success">Administrator</span> and its password.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #2</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-SMB2</span> with the following IP address <span className="label label-info">192.168.0.2</span> was vulnerable to a <span className="label label-danger">SMB</span> attack.
                    <br />
                    The attack succeeded by using a pass-the-hash attack over SMB protocol with user <span className="label label-success">temp</span>.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #3</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-WMI</span> with the following IP address <span className="label label-info">192.168.0.3</span> was vulnerable to a <span className="label label-danger">WMI</span> attack.
                    <br />
                    The attack succeeded by authenticating over WMI protocol with user <span className="label label-success">Administrator</span> and its password.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #4</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-WMI2</span> with the following IP address <span className="label label-info">192.168.0.4</span> was vulnerable to a <span className="label label-danger">WMI</span> attack.
                    <br />
                    The attack succeeded by using a pass-the-hash attack over WMI protocol with user <span className="label label-success">Administrator</span>.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #5</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-SSH</span> with the following IP address <span className="label label-info">192.168.0.5</span> was vulnerable to a <span className="label label-danger">SSH</span> attack.
                    <br />
                    The attack succeeded by authenticating over SSH protocol with user <span className="label label-success">user</span> and its password.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #6</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-RDP</span> with the following IP address <span className="label label-info">192.168.0.6</span> was vulnerable to a <span className="label label-danger">RDP</span> attack.
                    <br />
                    The attack succeeded by authenticating over RDP protocol with user <span className="label label-success">Administrator</span> and its password.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #7</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-SambaCry</span> with the following IP address <span className="label label-info">192.168.0.7</span> was vulnerable to a <span className="label label-danger">SambaCry</span> attack.
                    <br />
                    The attack succeeded by authenticating over SMB protocol with user <span className="label label-success">user</span> and its password, and by using the SambaCry vulnerability.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up.</li>
                      <li className="report">Use a complex one-use password that is not shared with other computers on the network.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #8</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-Elastic</span> with the following IP address <span className="label label-info">192.168.0.8</span> was vulnerable to an <span className="label label-danger">Elastic Groovy</span> attack.
                    <br />
                    The attack succeeded because the Elastic Search server was not parched against the CVE-2015-1427 bug.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Update your Elastic Search server to version 1.4.3 and up.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #9</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-Shellshock</span> with the following IP address <span className="label label-info">192.168.0.9</span> was vulnerable to a <span className="label label-danger">ShellShock</span> attack.
                    <br />
                    The attack succeeded because the HTTP server running on port <span className="label label-info">8080</span> was vulnerable to a shell injection attack on the paths: <span className="label label-warning">/cgi/backserver.cgi</span> <span className="label label-warning">/cgi/login.cgi</span>.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Update your Bash to a ShellShock-patched version.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #10</i></b></h4>
                  <p>
                    The machine <span className="label label-primary">Monkey-Conficker</span> with the following IP address <span className="label label-info">192.168.0.10</span> was vulnerable to a <span className="label label-danger">Conficker</span> attack.
                    <br />
                    The attack succeeded because the target machine uses an outdated and unpatched operating system vulnerable to Conficker.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Install the latest Windows updates or upgrade to a newer operating system.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #11</i></b></h4>
                  <p>
                    The network can probably be segmented. A monkey instance on <span className="label label-primary">Monkey-SMB</span> in the <span className="label label-info">192.168.0.0/24</span> network could directly access the Monkey Island C&C server in the <span className="label label-info">172.168.0.0/24</span> network.
                    <br />
                    In order to protect the network, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Segment your network. Make sure machines can't access machines from other segments.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #12</i></b></h4>
                  <p>
                    The network can probably be segmented. A monkey instance on <span className="label label-primary">Monkey-SSH</span> in the <span className="label label-info">192.168.0.0/24</span> network could directly access the Monkey Island C&C server in the <span className="label label-info">172.168.0.0/24</span> network.
                    <br />
                    In order to protect the network, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Segment your network. Make sure machines can't access machines from other segments.</li>
                    </ul>
                  </p>
                </div>
                <div>
                  <h4><b><i>Issue #13</i></b></h4>
                  <p>
                    Machines are not locked down at port level. Network tunnel was set up from <span className="label label-primary">Monkey-SSH</span> to <span className="label label-primary">Monkey-SambaCry</span>.
                    <br />
                    In order to protect the machine, the following steps should be performed:
                    <ul className="report">
                      <li className="report">Use micro-segmentation policies to disable communication other than the required.</li>
                    </ul>
                  </p>
                </div>
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
