import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';

class StartOverPageComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      cleaned: false
    };
  }

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Start Over</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            In order to reset the entire environment, all monkeys will be ordered to kill themselves
            and the database will be cleaned up.
          </p>
          <p>
            After that you could go back to the <Link to="/run-monkey">Run Monkey</Link> page to start new infections.
          </p>
          <p>
            <a onClick={this.cleanup} className="btn btn-danger btn-lg">Reset Environment</a>
          </p>
          { this.state.cleaned ?
            <div className="alert alert-info">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              Environment was reset successfully
            </div>
            : ''}
          <p>
            * BTW you can just continue and <Link to="/run-monkey">run more monkeys</Link> as you wish,
            and see the results on the <Link to="/infection/map">Infection Map</Link> without deleting anything.
          </p>
        </div>
      </Col>
    );
  }

  cleanup = () => {
    this.setState({
      cleaned: false
    });
    fetch('/api?action=reset')
      .then(res => res.json())
      .then(res => {
        if (res["status"] == "OK") {
          this.setState({
              cleaned: true
            });
        }
      });
  }
}

export default StartOverPageComponent;
