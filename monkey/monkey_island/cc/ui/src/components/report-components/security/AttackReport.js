import React from 'react';
import {Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import '../../../styles/Collapse.scss';
import AuthComponent from '../../AuthComponent';
import {ScanStatus} from "../../attack/techniques/Helpers";
import Collapse from '@kunukn/react-collapse';

import T1210 from '../../attack/techniques/T1210';
import T1197 from '../../attack/techniques/T1197';
import T1110 from '../../attack/techniques/T1110';
import T1075 from "../../attack/techniques/T1075";
import T1003 from "../../attack/techniques/T1003";
import T1059 from "../../attack/techniques/T1059";
import T1086 from "../../attack/techniques/T1086";
import T1082 from "../../attack/techniques/T1082";
import T1145 from "../../attack/techniques/T1145";
import T1105 from "../../attack/techniques/T1105";
import T1107 from "../../attack/techniques/T1107";
import T1065 from "../../attack/techniques/T1065";
import T1035 from "../../attack/techniques/T1035";
import T1129 from "../../attack/techniques/T1129";
import T1106 from "../../attack/techniques/T1106";
import T1188 from "../../attack/techniques/T1188";
import T1090 from "../../attack/techniques/T1090";
import T1041 from "../../attack/techniques/T1041";
import T1222 from "../../attack/techniques/T1222";
import T1005 from "../../attack/techniques/T1005";
import T1018 from "../../attack/techniques/T1018";
import T1016 from "../../attack/techniques/T1016";
import T1021 from "../../attack/techniques/T1021";
import T1064 from "../../attack/techniques/T1064";
import {extractExecutionStatusFromServerResponse} from "../common/ExecutionStatus";

const tech_components = {
  'T1210': T1210,
  'T1197': T1197,
  'T1110': T1110,
  'T1075': T1075,
  'T1003': T1003,
  'T1059': T1059,
  'T1086': T1086,
  'T1082': T1082,
  'T1145': T1145,
  'T1065': T1065,
  'T1105': T1105,
  'T1035': T1035,
  'T1129': T1129,
  'T1106': T1106,
  'T1107': T1107,
  'T1188': T1188,
  'T1090': T1090,
  'T1041': T1041,
  'T1222': T1222,
  'T1005': T1005,
  'T1018': T1018,
  'T1016': T1016,
  'T1021': T1021,
  'T1064': T1064
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
        this.setState(extractExecutionStatusFromServerResponse(res));
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
      case ScanStatus.SCANNED:
        return 'collapse-info';
      case ScanStatus.USED:
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
        <TechniqueComponent data={this.state.report[technique]} reportData={this.props.reportData}/>
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
        <section className="attack-report">{content}</section>
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
