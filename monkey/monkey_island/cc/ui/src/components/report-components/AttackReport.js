import React from 'react';
import {Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import AuthComponent from '../AuthComponent';
import Collapse from '@kunukn/react-collapse';
import T1210 from '../attack/techniques/T1210';
import T1197 from '../attack/techniques/T1197';
import T1110 from '../attack/techniques/T1110';
import '../../styles/Collapse.scss'

const tech_components = {
  'T1210': T1210,
  'T1197': T1197,
  'T1110': T1110
};

const classNames = require('classnames');

class AttackReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = {
      report: false,
      allMonkeysAreDead: false,
      runStarted: true,
      collapseOpen: ''
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

  onToggle = technique =>
    this.setState(state => ({ collapseOpen: state.collapseOpen === technique ? null : technique }));

  getComponentClass(tech_id){
    switch (this.state.report[tech_id].status) {
      case 'SCANNED':
        return 'collapse-info';
      case 'USED':
        return 'collapse-danger';
      default:
        return 'collapse-default';
    }
  }

  getTechniqueCollapse(tech_id){
    return (
      <div key={tech_id} className={classNames("collapse-item", { "item--active": this.state.collapseOpen === tech_id })}>
        <button className={classNames("btn-collapse", this.getComponentClass(tech_id))} onClick={() => this.onToggle(tech_id)}>
          <span>{this.state.report[tech_id].title}</span>
          <span>
              <i className={classNames("fa", this.state.collapseOpen === tech_id ? "fa-chevron-down" : "fa-chevron-up")}></i>
          </span>
        </button>
        <Collapse
          className="collapse-comp"
          isOpen={this.state.collapseOpen === tech_id}
          onChange={({ collapseState }) => {
            this.setState({ tech_id: collapseState });
          }}
          onInit={({ collapseState }) => {
            this.setState({ tech_id: collapseState });
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

  renderLegend() {
    return( <div id="header" className="row justify-content-between attack-legend">
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
            </div>)
  }

  generateReportContent(){
    let content = [];
    Object.keys(this.state.report).forEach((tech_id) => {
      content.push(this.getTechniqueCollapse(tech_id))
    });
    return (
      <div>
        {this.renderLegend()}
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
    return ( <div> {content} </div> );
  }
}

export default AttackReportPageComponent;
