import React from 'react';
import {Button, Col, Well, Nav, NavItem, Collapse, Form, FormControl, FormGroup} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import GridLoader from 'react-spinners/GridLoader';

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
      isAwsAuth: false,
      awsUpdateClicked: false,
      awsUpdateFailed: false,
      awsKeyId: '',
      awsSecretKey: '',
      awsMachines: [],
      is_loading_aws: true
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

    this.fetchAwsInfo();
    this.fetchConfig()
      .then(config => {
        this.setState({
          awsKeyId: config['cnc']['aws_config']['aws_access_key_id'],
          awsSecretKey: config['cnc']['aws_config']['aws_secret_access_key']
        });
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

  fetchAwsInfo() {
    return this.authFetch('/api/remote-monkey?action=list_aws')
      .then(res => res.json())
      .then(res =>{
        let is_aws = res['is_aws'];
        if (is_aws) {
          this.setState({isOnAws: true, awsMachines: res['instances'], isAwsAuth: res['auth'], is_loading_aws: false});
        }
      });
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

  updateAwsKeyId = (evt) => {
    this.setState({
      awsKeyId: evt.target.value
    });
  };

  updateAwsSecretKey = (evt) => {
    this.setState({
      awsSecretKey: evt.target.value
    });
  };

  fetchConfig() {
    return this.authFetch('/api/configuration/island')
      .then(res => res.json())
      .then(res => {
        return res.configuration;
      })
  }

  updateAwsKeys = () => {
    this.setState({
      awsUpdateClicked: true,
      awsUpdateFailed: false
    });
    this.fetchConfig()
      .then(config => {
        let new_config = config;
        new_config['cnc']['aws_config']['aws_access_key_id'] = this.state.awsKeyId;
        new_config['cnc']['aws_config']['aws_secret_access_key'] = this.state.awsSecretKey;
        return new_config;
      })
      .then(new_config => {
        this.authFetch('/api/configuration/island',
          {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(new_config)
          })
          .then(res => res.json())
          .then(res => {
            this.fetchAwsInfo()
              .then(res => {
                if (!this.state.isAwsAuth) {
                  this.setState({
                    awsUpdateClicked: false,
                    awsUpdateFailed: true
                  })
                }
              });
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

  renderAwsMachinesDiv() {
    return (
      <div style={{'marginBottom': '2em'}}>
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
        <div style={{'marginTop': '1em'}}>
          <button
            onClick={this.runOnAws}
            className={'btn btn-default btn-md center-block'}
            disabled={this.state.awsClicked}>
            Run on selected machines
            { this.state.awsClicked ? <Icon name="refresh" className="text-success" style={{'marginLeft': '5px'}}/> : null }
          </button>
        </div>
        <div style={{'marginTop': '1em'}}>
          <p>
            Not sure what this is? Not seeing your AWS EC2 instances? <a href="https://github.com/guardicore/monkey/wiki/Monkey-Island:-Running-the-monkey-on-AWS-EC2-instances}">Read the documentation</a>!
          </p>
        </div>
      </div>
    )
  }

  renderNotAuthAwsDiv() {
    return (
      <div style={{'marginBottom': '2em'}}>
        <p style={{'fontSize': '1.2em'}}>
          You haven't set your AWS account details or they're incorrect. Please enter them below to proceed.
        </p>
        <div style={{'marginTop': '1em'}}>
          <div className="col-sm-12">
          <div className="col-sm-6 col-sm-offset-3" style={{'fontSize': '1.2em'}}>
            <div className="panel panel-default">
              <div className="panel-body">
                <div className="input-group center-block text-center">
                  <input type="text" className="form-control" placeholder="AWS Access Key ID"
                         value={this.state.awsKeyId}
                         onChange={evt => this.updateAwsKeyId(evt)}/>
                  <input type="text" className="form-control" placeholder="AWS Secret Access Key"
                         value={this.state.awsSecretKey}
                         onChange={evt => this.updateAwsSecretKey(evt)}/>
                  <Button
                    onClick={this.updateAwsKeys}
                    className={'btn btn-default btn-md center-block'}
                    disabled={this.state.awsUpdateClicked}
                    variant="primary">
                    Update AWS details
                    { this.state.awsUpdateClicked ? <Icon name="refresh" className="text-success" style={{'marginLeft': '5px'}}/> : null }
                  </Button>
                </div>
              </div>
            </div>
          </div>
            <div className="col-sm-8 col-sm-offset-2" style={{'fontSize': '1.2em'}}>
              <p className="alert alert-info">
                <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
                In order to remotely run commands on AWS EC2 instances, please make sure you have
                the <a href="https://docs.aws.amazon.com/console/ec2/run-command/prereqs" target="_blank">prerequisites</a> and if the
                instances don't show up, check the
                AWS <a href="https://docs.aws.amazon.com/console/ec2/run-command/troubleshooting" target="_blank">troubleshooting guide</a>.
              </p>
            </div>
            {
              this.state.awsUpdateFailed ?
                <div className="col-sm-8 col-sm-offset-2" style={{'fontSize': '1.2em'}}>
                  <p className="alert alert-danger" role="alert">Authentication failed.</p>
                </div>
                :
                null
            }
          </div>
        </div>
      </div>
    )
  }

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
        /* TODO - How to center this component? */
        {
          this.state.is_loading_aws ?
            <p style={{'marginBottom': '2em', 'align': 'center'}}>
              <div className='sweet-loading'>
                <GridLoader
                  sizeUnit={"px"}
                  size={30}
                  color={'#ffcc00'}
                  loading={this.state.loading}
                />
              </div>
            </p>
             : null
        }
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
          {
            this.renderAwsMachinesDiv()
          }

        </Collapse>

        <p style={{'fontSize': '1.2em'}}>
          Go ahead and monitor the ongoing infection in the <Link to="/infection/map">Infection Map</Link> view.
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
