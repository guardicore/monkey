import React from 'react';
import {Col, Button} from 'react-bootstrap';
import '../../styles/Collapse.scss';
import '../../styles/report/AttackReport.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faCircle, faEye, faEyeSlash, faRadiation} from '@fortawesome/free-solid-svg-icons';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import {ScanStatus} from '../attack/techniques/Helpers';
import Matrix from './attack/ReportMatrixComponent';
import SelectedTechnique from './attack/SelectedTechnique';
import TechniqueDropdowns from './attack/TechniqueDropdowns';
import ReportLoader from './common/ReportLoader';

const techComponents = getAllAttackModules();

function getAllAttackModules() {
  let context = require.context("../attack/techniques/", false, /\.js$/);
  let obj = {};
  context.keys().forEach(function (key) {
    let techName = key.replace(/\.js/, '');
    techName = String(techName.replace(/\.\//, ''));
    obj[techName] = context(key).default;
  });
  return obj;
}

class AttackReport extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        selectedTechnique: false,
        collapseOpen: ''
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

  onTechniqueSelect = (technique, value) => {
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

  static getStatusIcon(tech_id, techniques){
    switch (techniques[tech_id].status){
      case ScanStatus.SCANNED:
        return <FontAwesomeIcon icon={faEye} className={"technique-status-icon"}/>;
      case ScanStatus.USED:
        return <FontAwesomeIcon icon={faRadiation} className={"technique-status-icon"}/>;
      default:
        return <FontAwesomeIcon icon={faEyeSlash} className={"technique-status-icon"}/>;
    }
  }

  renderLegend() {
    return (<div id='header' className='row justify-content-between attack-legend'>
      <Col xs={4}>
        <FontAwesomeIcon icon={faCircle} className='icon-default'/>
        <span> - Not scanned</span>
      </Col>
      <Col xs={4}>
        <FontAwesomeIcon icon={faCircle} className='icon-info'/>
        <span> - Scanned</span>
      </Col>
      <Col xs={4}>
        <FontAwesomeIcon icon={faCircle} className='icon-danger'/>
        <span> - Used</span>
      </Col>
    </div>)
  }

  generateReportContent() {
    return (
        <div id='attack' className='attack-report report-page'>
          <ReportHeader report_type={ReportTypes.attack}/>
          <hr/>
          <p>
            This report shows information about
            <Button bsStyle={'link'} href={'https://attack.mitre.org/'} bsSize={'lg'} className={'attack-link'}>Mitre ATT&CK™</Button>
            techniques used by Infection Monkey.
          </p>
          {this.renderLegend()}
          <Matrix techniques={this.state.techniques} schema={this.state.schema} onClick={this.onTechniqueSelect}/>
          <SelectedTechnique techComponents={techComponents}
                             techniques={this.state.techniques}
                             selected={this.state.selectedTechnique}/>
          <TechniqueDropdowns techniques={this.state.techniques}
                              techComponents={techComponents}
                              schema={this.state.schema}/>
          <br/>
        </div>
    )
  }

  getTechniqueByTitle(title){
    for (const tech_id in this.state.techniques){
      if (! this.state.techniques.hasOwnProperty(tech_id)) {return false;}
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
    for(const type in schema){
      if (! schema.hasOwnProperty(type)) {return false;}
      let typeTechniques = schema[type].properties;
      for(const tech_id in typeTechniques){
        if (! typeTechniques.hasOwnProperty(tech_id)) {return false;}
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
