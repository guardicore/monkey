import React from 'react';
import {css} from '@emotion/core';
import {Button, Col, Card, Nav, Collapse} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import GridLoader from 'react-spinners/GridLoader';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClipboard} from '@fortawesome/free-solid-svg-icons/faClipboard';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faSync} from '@fortawesome/free-solid-svg-icons/faSync';
import {faInfoCircle} from "@fortawesome/free-solid-svg-icons/faInfoCircle";
import {faExclamationTriangle} from "@fortawesome/free-solid-svg-icons/faExclamationTriangle";

import {Link} from 'react-router-dom';
import AuthComponent from '../AuthComponent';
import AwsRunTable from '../run-monkey/AwsRunTable';

import MissingBinariesModal from '../ui-components/MissingBinariesModal';

import '../../styles/MonkeyRunPage.scss';

const loading_css_override = css`
    display: block;
    margin-right: auto;
    margin-left: auto;
`;

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
      awsUpdateClicked: false,
      awsUpdateFailed: false,
      awsMachines: [],
      isLoadingAws: true,
      isErrorWhileCollectingAwsMachines: false,
      awsMachineCollectionErrorMsg: '',
      showModal: false,
      errorDetails: ''
    };

    this.closeModal = this.closeModal.bind(this);
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
      .then(res => {
        if (res['is_running']) {
          this.setState({runningOnIslandState: 'running'});
        } else {
          this.setState({runningOnIslandState: 'not_running'});
        }
      });

    this.fetchAwsInfo();
    this.fetchConfig();

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
      .then(res => {
        let is_aws = res['is_aws'];
        if (is_aws) {
          // On AWS!
          // Checks if there was an error while collecting the aws machines.
          let is_error_while_collecting_aws_machines = (res['error'] != null);
          if (is_error_while_collecting_aws_machines) {
            // There was an error. Finish loading, and display error message.
            this.setState({
              isOnAws: true,
              isErrorWhileCollectingAwsMachines: true,
              awsMachineCollectionErrorMsg: res['error'],
              isLoadingAws: false
            });
          } else {
            // No error! Finish loading and display machines for user
            this.setState({isOnAws: true, awsMachines: res['instances'], isLoadingAws: false});
          }
        } else {
          // Not on AWS. Finish loading and don't display the AWS div.
          this.setState({isOnAws: false, isLoadingAws: false});
        }
      });
  }

  static generateLinuxCmd(ip, is32Bit) {
    let bitText = is32Bit ? '32' : '64';
    return `wget --no-check-certificate https://${ip}:5000/api/monkey/download/monkey-linux-${bitText}; chmod +x monkey-linux-${bitText}; ./monkey-linux-${bitText} m0nk3y -s ${ip}:5000`
  }

  static generateWindowsCmd(ip, is32Bit) {
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
          /* If Monkey binaries are missing, change the state accordingly */
          if (res['error_text'].startsWith('Copy file failed')) {
            this.setState({
              showModal: true,
              errorDetails: res['error_text']}
            );
          }
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
      cmdText = RunMonkeyPageComponent.generateLinuxCmd(this.state.selectedIp, is32Bit);
    } else {
      cmdText = RunMonkeyPageComponent.generateWindowsCmd(this.state.selectedIp, is32Bit);
    }
    return (
      <Card key={'cmdDiv' + this.state.selectedIp} style={{'margin': '0.5em'}}>
        <div style={{'overflow': 'auto', 'padding': '0.5em'}}>
          <CopyToClipboard text={cmdText} className="pull-right btn-sm">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <FontAwesomeIcon icon={faClipboard}/>
            </Button>
          </CopyToClipboard>
          <code>{cmdText}</code>
        </div>
      </Card>
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

  static renderIconByState(state) {
    if (state === 'running') {
      return (<FontAwesomeIcon icon={faCheck} className="text-success" style={{'marginLeft': '5px'}}/>)
    } else if (state === 'installing') {
      return (<FontAwesomeIcon icon={faSync} className="text-success" style={{'marginLeft': '5px'}}/>)
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

  fetchConfig() {
    return this.authFetch('/api/configuration/island')
      .then(res => res.json())
      .then(res => {
        return res.configuration;
      })
  }

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
        <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
          <p className="alert alert-info">
            <FontAwesomeIcon icon={faInfoCircle} style={{'marginRight': '5px'}}/>
            Not sure what this is? Not seeing your AWS EC2 instances? <a
            href="https://github.com/guardicore/monkey/wiki/Monkey-Island:-Running-the-monkey-on-AWS-EC2-instances"
            rel="noopener noreferrer" target="_blank">Read the documentation</a>!
          </p>
        </div>
        {
          this.state.ips.length > 1 ?
            <Nav variant="pills" activeKey={this.state.selectedIp} onSelect={this.setSelectedIp}
                 style={{'marginBottom': '2em'}}>
              {this.state.ips.map(ip => <Nav.Item><Nav.Link eventKey={ip}>{ip}</Nav.Link></Nav.Item>)}
            </Nav>
            : <div style={{'marginBottom': '2em'}}/>
        }

        <AwsRunTable
          data={this.state.awsMachines}
          ref={r => (this.awsTable = r)}
        />
        <div style={{'marginTop': '1em'}}>
          <Button
            onClick={this.runOnAws}
            className={'btn btn-default btn-md center-block'}
            disabled={this.state.awsClicked}>
            Run on selected machines
            {this.state.awsClicked ?
              <FontAwesomeIcon icon={faSync} className="text-success" style={{'marginLeft': '5px'}}/> : null}
          </Button>
        </div>
      </div>
    )
  }

  closeModal = () => {
    this.setState({
      showModal: false
    })
  };

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">2. Run the Monkey</h1>
        <p style={{'marginBottom': '2em', 'fontSize': '1.2em'}}>
          Go ahead and run the monkey!
          <i> (Or <Link to="/configure">configure the monkey</Link> to fine tune its behavior)</i>
        </p>
        <p className={'text-center'}>
          <Button onClick={this.runLocalMonkey}
                  variant={'outline-monkey'}
                  size='lg'
                  disabled={this.state.runningOnIslandState !== 'not_running'}
          >
            Run on Monkey Island Server
            {RunMonkeyPageComponent.renderIconByState(this.state.runningOnIslandState)}
          </Button>
          <MissingBinariesModal
                        showModal = {this.state.showModal}
                        onClose = {this.closeModal}
                        errorDetails = {this.state.errorDetails}/>
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
        <p className={'text-center'}
           style={this.state.showManual || !this.state.isOnAws ? {'marginBottom': '2em'} : {}}>
          <Button onClick={this.toggleManual}
                  variant={'outline-monkey'}
                  size='lg'
                  className={(this.state.showManual ? 'active' : '')}>
            Run on a machine of your choice
          </Button>
        </p>
        <Collapse in={this.state.showManual}>
          <div style={{'marginBottom': '2em'}}>
            <p style={{'fontSize': '1.2em'}}>
              Choose the operating system where you want to run the monkey
              {this.state.ips.length > 1 ? ', and the interface to communicate with.' : '.'}
            </p>
            <Nav variant='pills' id={'bootstrap-override'} className={'run-on-os-buttons'}
                 activeKey={this.state.selectedOs} onSelect={this.setSelectedOs}>
              <Nav.Item>
                <Nav.Link eventKey={'windows-32'}>
                  Windows (32 bit)
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey='windows-64'>
                  Windows (64 bit)
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey='linux-32' variant={'monkey-alt'}>
                  Linux (32 bit)
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey='linux-64'>
                  Linux (64 bit)
                </Nav.Link>
              </Nav.Item>
            </Nav>
            {this.state.ips.length > 1 ?
              <Nav variant="pills" activeKey={this.state.selectedIp} onSelect={this.setSelectedIp}
                   className={'run-on-os-buttons'}>
                {this.state.ips.map(ip => <Nav.Item>
                  <Nav.Link eventKey={ip}>{ip}</Nav.Link></Nav.Item>)}
              </Nav>
              : <div style={{'marginBottom': '2em'}}/>
            }
            <p style={{'fontSize': '1.2em'}}>
              Copy the following command to your machine and run it with Administrator or root privileges.
            </p>
            {this.generateCmdDiv()}
          </div>
        </Collapse>
        {
          this.state.isLoadingAws ?
            <div style={{'marginBottom': '2em', 'align': 'center'}}>
              <div className='sweet-loading'>
                <GridLoader
                  css={loading_css_override}
                  sizeUnit={'px'}
                  size={30}
                  color={'#ffcc00'}
                  loading={this.state.loading}
                />
              </div>
            </div>
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
            <p style={{'marginBottom': '2em'}} className={'text-center'}>
              <Button onClick={this.toggleAws}
                      className={(this.state.showAws ? ' active' : '')}
                      size='lg'
                      variant={'outline-monkey'}>
                Run on AWS machine of your choice
              </Button>
            </p>
            :
            null
        }
        <Collapse in={this.state.showAws}>
          {
            this.state.isErrorWhileCollectingAwsMachines ?
              <div style={{'marginTop': '1em'}}>
                <p className="alert alert-danger">
                  <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
                  Error while collecting AWS machine data. Error
                  message: <code>{this.state.awsMachineCollectionErrorMsg}</code><br/>
                  Are you sure you've set the correct role on your Island AWS machine?<br/>
                  Not sure what this is? <a
                  href="https://github.com/guardicore/monkey/wiki/Monkey-Island:-Running-the-monkey-on-AWS-EC2-instances">Read
                  the documentation</a>!
                </p>
              </div>
              :
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
