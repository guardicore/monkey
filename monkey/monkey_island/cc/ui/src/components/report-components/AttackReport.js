import React from 'react';
import {Col} from 'react-bootstrap';
import '../../styles/Collapse.scss';
import '../../styles/report/AttackReport.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle as faCircle } from '@fortawesome/free-solid-svg-icons';
import { faCircle as faCircleThin } from '@fortawesome/free-regular-svg-icons';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import {ScanStatus} from '../attack/techniques/Helpers';
import Matrix from './attack/ReportMatrix';
import SelectedTechnique from './attack/SelectedTechnique';
import TechniqueDropdowns from './attack/TechniqueDropdowns';
import ReportLoader from './common/ReportLoader';

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

const techComponents = {
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


class AttackReport extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        selectedTechnique: false,
        collapseOpen: '',
    };
    if (typeof this.props.report.schema !== 'undefined' && typeof this.props.report.techniques !== 'undefined'){
      this.state['schema'] = this.props.report['schema'];
      this.state['techniques'] = AttackReport.addLinksToTechniques(this.props.report['schema'], this.props.report['techniques']);
    }
  }

  componentDidUpdate(prevProps) {
    if (this.props.report !== prevProps.report) {
     this.setState({schema: this.props.report['schema'],
      techniques: AttackReport.addLinksToTechniques(this.props.report['schema'], this.props.report['techniques'])})
    }
  }

  onTechniqueSelect = (technique, value, mapped = false) => {
    //this.setState({selectedTechnique: technique});
    let selectedTechnique = this.getTechniqueByTitle(technique);
    if (selectedTechnique === false){
      return;
    }
    this.setState({selectedTechnique: selectedTechnique.tech_id})
  };

  static getComponentClass(tech_id, techniques) {
    switch (techniques[tech_id].status) {
      case ScanStatus.SCANNED:
        return 'collapse-info';
      case ScanStatus.USED:
        return 'collapse-danger';
      default:
        return 'collapse-default';
    }
  }

  renderLegend() {
    return (<div id="header" className="row justify-content-between attack-legend">
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircleThin} className="icon-unchecked"/>
        <span> - Dissabled</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className="icon-default"/>
        <span> - Unscanned</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className="icon-info"/>
        <span> - Scanned</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className="icon-danger"/>
        <span> - Used</span>
      </Col>
    </div>)
  }

  generateReportContent() {
    return (
        <div id="attack" className="attack-report report-page">
          <ReportHeader report_type={ReportTypes.attack}/>
          <hr/>
          <p>
            This report shows information about ATT&CK techniques used by Infection Monkey.
          </p>
          {this.renderLegend()}
          <Matrix techniques={this.state.techniques} schema={this.state.schema} onClick={this.onTechniqueSelect}/>
          <SelectedTechnique techComponents={techComponents}
                             techniques={this.state.techniques}
                             selected={this.state.selectedTechnique}/>
          <TechniqueDropdowns techniques={this.state.techniques}
                              techComponents={techComponents}/>
          <br/>
        </div>
    )
  }

  getTechniqueByTitle(title){
    for (let tech_id in this.state.techniques){
      let technique = this.state.techniques[tech_id];
      if (technique.title === title){
        technique['tech_id'] = tech_id;
        return technique
      }
    }
    return false;
  }

  static addLinksToTechniques(schema, techniques){
    schema = schema.properties;
    for(let type in schema){
      let typeTechniques = schema[type].properties;
      for(let tech_id in typeTechniques){
        if (typeTechniques[tech_id] !== undefined){
          techniques[tech_id]['link'] = typeTechniques[tech_id].link
        }
      }
    }
    return techniques
  }

  render() {
    if (typeof this.state.schema === 'undefined' || typeof this.state.techniques === 'undefined') {
      return (<ReportLoader/>);
    } else {
      return (<div> {this.generateReportContent()}</div>);
    }
  }
}

export default AttackReport;
