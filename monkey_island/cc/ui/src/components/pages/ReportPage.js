import React from 'react';
import {Col} from 'react-bootstrap';
import BreachedServers from 'components/report-components/BreachedServers';
import ScannedServers from 'components/report-components/ScannedServers';

const list_item = {
  label: 'machine 1',
  ip_addresses: ['1.2.3.4', '5.6.7.8'],
  accessible_from_nodes: ['machine 2', 'machine 3'],
  services: ['tcp-80', 'tcp-443']
};

class ReportPageComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      report: {}
    };
  }

  componentDidMount() {
    fetch('/api/report')
      .then(res => res.json())
      .then(res => {
        this.setState({
          report: res
        });
      });
  }

  render() {
    if (Object.keys(this.state.report).length === 0) {
      return (<div></div>);
    }
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">4. Security Report</h1>
        <div style={{'fontSize': '1.2em'}}>
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
              {/* TODO: Add map */}
            </p>
            <div>
              <h3>* Imagine Map here :) *</h3>
            </div>
            <div>
              {/* TODO: Replace 3 with data */}
              During this simulated attack the Monkey uncovered <span className="label label-warning">3 issues</span>, detailed below. The security issues uncovered included:
              <ul className="report">
                {/* TODO: Replace lis with data */}
                <li className="report">Weak user/passwords combinations</li>
                <li className="report">Machines not patched for the ‘Shellshock’ bug</li>
              </ul>
            </div>
            <div>
              In addition, the monkey uncovered the following possible set of issues:
              <ul className="report">
                {/* TODO: Replace lis with data */}
                <li className="report">Machines from another segment accessed the Monkey Island</li>
                <li className="report">Network tunnels were created successfully</li>
              </ul>
            </div>
            <p>
              A full report of the Monkeys activities follows.
            </p>
          </div>
          <div id="network_overview">
            <h1>
              Network Overview
            </h1>
            <p>
              {/* TODO: Replace 6,2 with data */}
              During the current run, the Monkey discovered <span className="label label-info">6</span> machines and successfully breached <span className="label label-warning">2</span> of them.
              In addition, it attempted to exploit the rest, any security software installed in the network should have picked up the attack attempts and logged them.
            </p>
            <div>
              Detailed recommendations in the next part of the <a href="#recommendations">report</a>.
              <h4>Breached Servers</h4>
              <BreachedServers data={this.state.report.exploited}></BreachedServers>
            </div>
            <div>
              <h4>Scanned Servers</h4>
              <ScannedServers data={this.state.report.scanned}></ScannedServers>
              {/* TODO: Add table of scanned servers */}
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
                  The machine <span className="label label-primary">Monkey-SMB</span> with the following IP addresses <span className="label label-info">192.168.0.1</span> <span className="label label-info">10.0.0.18</span> was vulnerable to a <span className="label label-danger">SmbExploiter</span> attack.
                  The attack succeeded because weak/stolen password was used over SMB protocol.
                </p>
              </div>
              <div>
                <h4><b><i>Issue #2</i></b></h4>
                <p>
                  The network can probably be segmented. A monkey instance on <span className="label label-primary">Monkey-SMB</span> in the <span className="label label-info">192.168.0.0/24</span> network could directly access the Monkey Island C&C server in the <span className="label label-info">172.168.0.0/24</span> network.
                </p>
              </div>
            </div>
            {/* TODO: Entire part */}
          </div>
        </div>
      </Col>
    );
  }
}

export default ReportPageComponent;
