import React from 'react';
import {Button, Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';
import T1210 from '../attack/T1210'

class AttackReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      report: {},
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  componentDidMount() {
    this.updateMonkeysRunning().then(res => this.getReportFromServer(res));
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done']),
          runStarted: res['completed_steps']['run_monkey']
        });
        return res;
      });
  };

  getReportFromServer(res) {
    if (res['completed_steps']['run_monkey']) {
      this.authFetch('/api/attack/report')
        .then(res => res.json())
        .then(res => {
          this.setState({
            report: res
          });
        });
    }
  }

  generateReportContent(){
    let content = '';
    Object.keys(this.state.report).forEach((Technique) => {
      content = <T1210 data={this.state.report[Technique]} />;
    });
    return content
  }

  render() {
    console.log(React.version);
    let content;
    if (Object.keys(this.state.report).length === 0) {
      if (this.state.runStarted) {
        content = (<h1>Generating Report...</h1>);
      } else {
        content =
          <p className="alert alert-warning">
            <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
            You have to run a monkey before generating a report!
          </p>;
      }
    } else {
      content = this.generateReportContent();
    }
    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title no-print">5. ATT&CK Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }
}

export default AttackReportPageComponent;
