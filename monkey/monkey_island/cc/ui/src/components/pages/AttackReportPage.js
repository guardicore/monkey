import React from 'react';
import {Button, Col, Row, TabContainer} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';
import Collapse from '@kunukn/react-collapse';
import T1210 from '../attack/T1210';
import '../../styles/Collapse.scss'

const tech_components = {
  'T1210': T1210
};

const classNames = require('classnames');

class AttackReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      report: false,
      allMonkeysAreDead: false,
      runStarted: true,
      index: 1
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

  onToggle = index =>
    this.setState(state => ({ index: state.index === index ? null : index }));

  getTechniqueCollapse(tech_id){
    switch (this.state.report[tech_id].status) {
      case 'SCANNED':
        var className = 'collapse-info';
        break;
      case 'USED':
        var className = 'collapse-danger';
        break;
      default:
        var className = 'collapse-default';
    }

    return (
      <div className={classNames("collapse-item", { "item--active": this.state.index === 1 })}>
        <button className={classNames("btn-collapse", className)} onClick={() => this.onToggle(1)}>
          <span>{this.state.report[tech_id].title}</span>
          <span>
              <i className={classNames("fa", this.state.index === 1 ? "fa-chevron-down" : "fa-chevron-up")}></i>
          </span>
        </button>
        <Collapse
          className="collapse-comp"
          isOpen={this.state.index === 1}
          onChange={({ collapseState }) => {
            this.setState({ item1: collapseState });
          }}
          onInit={({ collapseState }) => {
            this.setState({ item1: collapseState });
          }}
          render={collapseState => this.createTechniqueContent(collapseState, tech_id)}/>
      </div>
    );
  }

  createTechniqueContent(collapseState, technique) {
    const TechniqueComponent = tech_components[technique];
    return (
      <div className={`content ${collapseState}`}>
        <TechniqueComponent data={this.state.report[technique]} />
      </div>
    );
  }

  generateReportContent(){
    let content = '';
    Object.keys(this.state.report).forEach((tech_id) => {
      content = this.getTechniqueCollapse(tech_id)
    });
    return (
      <div>
        <div id="header" className="row justify-content-between attack-legend">
          <Col xs={4}>
            <i className="fa fa-circle icon-default"></i>
            <span> - Unscanned</span>
          </Col>
          <Col xs={4}>
            <i className="fa fa-circle icon-info"></i>
            <span> - Scanned</span>
          </Col>
          <Col xs={4}>
            <i className="fa fa-circle icon-danger"></i>
            <span> - Used</span>
          </Col>
        </div>
        <section className="app">{content}</section>
      </div>
    )
  }

  render() {
    let content;
    if (! this.state.runStarted)
    {
      content =
        <p className="alert alert-warning">
          <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
          You have to run a monkey before generating a report!
        </p>;
    } else if (this.state.report === false){
        content = (<h1>Generating Report...</h1>);
    } else if (Object.keys(this.state.report).length === 0) {
      if (this.state.runStarted) {
        content = (<h1>No techniques were scanned</h1>);
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
