import React from 'react';
import {Col} from 'react-bootstrap';
import {ReactiveGraph} from 'components/reactive-graph/ReactiveGraph';
import {edgeGroupToColor, options} from 'components/map/MapOptions';
import '../../styles/Collapse.scss';
import AuthComponent from '../AuthComponent';
import {ScanStatus} from '../attack/techniques/Helpers';
import Collapse from '@kunukn/react-collapse';

import T1210 from '../attack/techniques/T1210';
import T1197 from '../attack/techniques/T1197';
import T1110 from '../attack/techniques/T1110';
import T1075 from '../attack/techniques/T1075';
import T1003 from '../attack/techniques/T1003';
import T1059 from '../attack/techniques/T1059';
import T1086 from '../attack/techniques/T1086';
import T1082 from '../attack/techniques/T1082';
import T1145 from '../attack/techniques/T1145';
import T1105 from '../attack/techniques/T1105';
import T1107 from '../attack/techniques/T1107';
import T1065 from '../attack/techniques/T1065';
import T1035 from '../attack/techniques/T1035';
import T1129 from '../attack/techniques/T1129';
import T1106 from '../attack/techniques/T1106';
import T1188 from '../attack/techniques/T1188';
import T1090 from '../attack/techniques/T1090';
import T1041 from '../attack/techniques/T1041';
import T1222 from '../attack/techniques/T1222';
import T1005 from '../attack/techniques/T1005';
import T1018 from '../attack/techniques/T1018';
import T1016 from '../attack/techniques/T1016';
import T1021 from '../attack/techniques/T1021';
import T1064 from '../attack/techniques/T1064';

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
      report: this.props.report,
      collapseOpen: ''
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props.report !== prevProps.report) {
     this.setState({ report: this.props.report })
    }
  }

  onToggle = technique =>
    this.setState(state => ({collapseOpen: state.collapseOpen === technique ? null : technique}));

  getComponentClass(tech_id) {
    switch (this.state.report[tech_id].status) {
      case ScanStatus.SCANNED:
        return 'collapse-info';
      case ScanStatus.USED:
        return 'collapse-danger';
      default:
        return 'collapse-default';
    }
  }

  getTechniqueCollapse(tech_id) {
    return (
      <div key={tech_id} className={classNames('collapse-item', {'item--active': this.state.collapseOpen === tech_id})}>
        <button className={classNames('btn-collapse', this.getComponentClass(tech_id))} onClick={() => this.onToggle(tech_id)}>
          <span>{this.state.report[tech_id].title}</span>
          <span>
              <i className={classNames('fa', this.state.collapseOpen === tech_id ? 'fa-chevron-down' : 'fa-chevron-up')}></i>
          </span>
        </button>
        <Collapse
          className="collapse-comp"
          isOpen={this.state.collapseOpen === tech_id}
          onChange={({collapseState}) => {
            this.setState({tech_id: collapseState});
          }}
          onInit={({collapseState}) => {
            this.setState({tech_id: collapseState});
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
    return (<div id="header" className="row justify-content-between attack-legend">
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

  generateReportContent() {
    let content = [];
    Object.keys(this.state.report).forEach((tech_id) => {
      content.push(this.getTechniqueCollapse(tech_id))
    });
    return (
      <div id="attack">
      <h3>
        ATT&CK report
      </h3>
      <p>
        This report shows information about ATT&CK techniques used by Infection Monkey.
      </p>
      <div>
        {this.renderLegend()}
        <section className="attack-report">{content}</section>
      </div>
      <br/>
    </div>
    )
  }

  render() {
    if (Object.keys(this.state.report).length === 0 && this.state.runStarted) {
        return (<h1>No techniques were scanned</h1>);
    } else {
      return (<div> {this.generateReportContent()}</div>);
    }
  }
}

export default AttackReportPageComponent;
