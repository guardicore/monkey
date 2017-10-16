import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';

class RunServerPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {ip: '0.0.0.0'};
  }

  componentDidMount() {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({ip: res['ip_addresses'][0]}));
  }

  render() {
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">Monkey Island C&C Server</h1>
        <div style={{'fontSize': '1.5em'}}>
          <p>Your Monkey Island server is up and running on <b>{this.state.ip}</b> &#x1F44F; &#x1F44F;</p>
          <p>
            Go ahead and <Link to="/run-monkey">run the monkey</Link>.
          </p>
          <p style={{'marginTop': '30px'}}>
            <i>(You can make further adjustments by <Link to="/configure">configuring the monkey</Link>)</i>
          </p>
        </div>
      </Col>
    );
  }
}

export default RunServerPageComponent;
