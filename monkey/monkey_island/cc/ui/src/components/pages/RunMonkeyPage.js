import React from 'react';
import {Button, Col, Well, Nav, NavItem, Collapse} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {Icon} from 'react-fa';
import {Link} from 'react-router-dom';
import AuthComponent from '../AuthComponent';
import AwsRunTable from "../run-monkey/AwsRunTable";

class RunMonkeyPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      ips: [],
      runningOnIslandState: 'not_running',
      runningOnClientState: 'not_running',
      awsClicked: false,
      selectedIp: '0.0.0.0',
      selectedOs: 'windows-32',
      showManual: false,
      showAws: false,
      isOnAws: false,
      awsMachines: []
    };
  }

  componentDidMount() {
    this.authFetch('/api')
      .then(res => res.json())
      .then(res => this.setState({
        ips: res['ip_addresses'],
        selectedIp: res['ip_addresses'][0]
      }));

    this.authFetch('/api/local-monkey')
      .then(res => res.json())
      .then(res =>{
        if (res['is_running']) {
          this.setState({runningOnIslandState: 'running'});
        } else {
          this.setState({runningOnIslandState: 'not_running'});
        }
      });

    this.authFetch('/api/remote-monkey?action=list_aws')
      .then(res => res.json())
      .then(res =>{
        let is_aws = res['is_aws'];
        if (is_aws) {
          let instances = res['instances'];
          if (instances) {
            this.setState({isOnAws: true, awsMachines: instances});
          }
        }
      });

    this.authFetch('/api/client-monkey')
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
    return `wget --no-check-certificate https://${ip}:5000/api/monkey/download/monkey-linux-${bitText}; chmod +x monkey-linux-${bitText}; ./monkey-linux-${bitText} m0nk3y -s ${ip}:5000`
  }

  generateWindowsCmd(ip, is32Bit) {
    let bitText = is32Bit ? '32' : '64';
    return `powershell [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}; (New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/monkey/download/monkey-windows-${bitText}.exe','.\\monkey.exe'); ;Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`;
  }

  runLocalMonkey = () => {
    this.authFetch('/api/local-monkey',
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

  generateCmdDiv() {
    let isLinux = (this.state.selectedOs.split('-')[0] === 'linux');
    let is32Bit = (this.state.selectedOs.split('-')[1] === '32');
    let cmdText = '';
    if (isLinux) {
      cmdText = this.generateLinuxCmd(this.state.selectedIp, is32Bit);
    } else {
      cmdText = this.generateWindowsCmd(this.state.selectedIp, is32Bit);
    }
    return (
      <Well key={'cmdDiv'+this.state.selectedIp} className="well-sm" style={{'margin': '0.5em'}}>
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

  setSelectedOs = (key) => {
    this.setState({
      selectedOs: key
    });
  };

  setSelectedIp = (key) => {
    this.setState({
      selectedIp: key
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

  toggleManual = () => {
    this.setState({
      showManual: !this.state.showManual
    });
  };

  toggleAws = () => {
    this.setState({
      showAws: !this.state.showAws
    });
  };

  runOnAws = () => {
    this.setState({
      awsClicked: true
    });

    let instances = this.awsTable.state.selection.map(x => this.instanceIdToInstance(x));

    this.authFetch('/api/remote-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: 'aws', instances: instances, island_ip: this.state.selectedIp})
      }).then(res => res.json())
      .then(res => {
        let result = res['result'];

        // update existing state, not run-over
        let prevRes = this.awsTable.state.result;
        for (let key in result) {
          if (result.hasOwnProperty(key)) {
            prevRes[key] = result[key];
          }
        }
        this.awsTable.setState({
          result: prevRes,
          selection: [],
          selectAll: false
        });

        this.setState({
          awsClicked: false
        });
      });
  };

  instanceIdToInstance = (instance_id) => {
    let instance = this.state.awsMachines.find(
      function (inst) {
        return inst['instance_id'] === instance_id;
      });
    return {'instance_id': instance_id, 'os': instance['os']}

  };

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">2. Run the Monkey</h1>
        <p style={{'marginBottom': '2em', 'fontSize': '1.2em'}}>
          Go ahead and run the monkey!
          <i> (Or <Link to="/configure">configure the monkey</Link> to fine tune its behavior)</i>
        </p>
        <p>
          <button onClick={this.runLocalMonkey}
                  className="btn btn-default btn-lg center-block"
                  disabled={this.state.runningOnIslandState !== 'not_running'}
                  >
            Run on Monkey Island Server
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
        <p className="text-center">
          OR
        </p>
        <p style={this.state.showManual || !this.state.isOnAws ? {'marginBottom': '2em'} : {}}>
          <button onClick={this.toggleManual} className={'btn btn-default btn-lg center-block' + (this.state.showManual ? ' active' : '')}>
            Run on machine of your choice
          </button>
        </p>
        <Collapse in={this.state.showManual}>
          <div style={{'marginBottom': '2em'}}>
            <p style={{'fontSize': '1.2em'}}>
              Choose the operating system where you want to run the monkey
              {this.state.ips.length > 1 ? ', and the interface to communicate with.' : '.'}
            </p>
            <Nav bsStyle="pills" justified activeKey={this.state.selectedOs} onSelect={this.setSelectedOs}>
              <NavItem key='windows-32' eventKey='windows-32'>Windows (32 bit)</NavItem>
              <NavItem key='windows-64' eventKey='windows-64'>Windows (64 bit)</NavItem>
              <NavItem key='linux-32' eventKey='linux-32'>Linux (32 bit)</NavItem>
              <NavItem key='linux-64' eventKey='linux-64'>Linux (64 bit)</NavItem>
            </Nav>
            {this.state.ips.length > 1 ?
              <Nav bsStyle="pills" justified activeKey={this.state.selectedIp} onSelect={this.setSelectedIp}
                   style={{'marginBottom': '2em'}}>
                {this.state.ips.map(ip => <NavItem key={ip} eventKey={ip}>{ip}</NavItem>)}
              </Nav>
              : <div style={{'marginBottom': '2em'}} />
            }
            <p style={{'fontSize': '1.2em'}}>
              Copy the following command to your machine and run it with Administrator or root privileges.
            </p>
            {this.generateCmdDiv()}
          </div>
        </Collapse>
        {
          this.state.isOnAws ?
            <p className="text-center">
              OR
            </p>
            :
            null
        }
        {
          this.state.isOnAws ?
            <p style={{'marginBottom': '2em'}}>
              <button onClick={this.toggleAws} className={'btn btn-default btn-lg center-block' + (this.state.showAws ? ' active' : '')}>
                Run on AWS machine of your choice
              </button>
            </p>
            :
            null
        }
        <Collapse in={this.state.showAws}>
          <div style={{'marginBottom': '2em'}}>
            <p style={{'fontSize': '1.2em'}}>
              Select server IP address
            </p>
            {
              this.state.ips.length > 1 ?
              <Nav bsStyle="pills" justified activeKey={this.state.selectedIp} onSelect={this.setSelectedIp}
                   style={{'marginBottom': '2em'}}>
                {this.state.ips.map(ip => <NavItem key={ip} eventKey={ip}>{ip}</NavItem>)}
              </Nav>
              : <div style={{'marginBottom': '2em'}} />
            }

            <AwsRunTable
              data={this.state.awsMachines}
              ref={r => (this.awsTable = r)}
            />
            <button
              onClick={this.runOnAws}
              className={'btn btn-default btn-md center-block'}
              disabled={this.state.awsClicked}>
              Run on selected machines
              { this.state.awsClicked ? <Icon name="refresh" className="text-success" style={{'marginLeft': '5px'}}/> : null }
            </button>
          </div>
        </Collapse>

        <p style={{'fontSize': '1.2em'}}>
          Go ahead and monitor the ongoing infection in the <Link to="/infection/map">Infection Map</Link> view.
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
