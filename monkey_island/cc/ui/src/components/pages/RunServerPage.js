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
        <div style={{'fontSize': '1.2em'}}>
          <p style={{'marginTop': '30px'}}>Congrats! You have successfully set up the Monkey Island server. &#x1F44F; &#x1F44F;</p>
          <p>
            The Infection Monkey is an open source security tool for testing a data center's resiliency to perimeter
            breaches and internal server infection.
            The Monkey uses various methods to self propagate across a data
            center and reports success to a centralized C&C server.
            To read more about the Monkey, visit <a href="http://infectionmonkey.com" target="_blank">infectionmonkey.com</a>
          </p>
          <p>
            Go ahead and <Link to="/run-monkey">run the monkey</Link>.
          </p>
        </div>
      </Col>
    );
  }
}

export default RunServerPageComponent;
