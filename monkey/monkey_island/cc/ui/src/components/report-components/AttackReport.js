import React from 'react';
import {Col, Button} from 'react-bootstrap';
import '../../styles/components/Collapse.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faCircle} from '@fortawesome/free-solid-svg-icons/faCircle';
import {faRadiation} from '@fortawesome/free-solid-svg-icons/faRadiation';
import {faEye} from '@fortawesome/free-solid-svg-icons/faEye';
import {faEyeSlash} from '@fortawesome/free-solid-svg-icons/faEyeSlash';
import {faToggleOff} from '@fortawesome/free-solid-svg-icons/faToggleOff';
import marked from 'marked';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import {ScanStatus} from '../attack/techniques/Helpers';
import Matrix from './attack/ReportMatrixComponent';
import SelectedTechnique from './attack/SelectedTechnique';
import TechniqueDropdowns from './attack/TechniqueDropdowns';
import ReportLoader from './common/ReportLoader';

const techComponents = getAllAttackModules();

function getAllAttackModules() {
  let context = require.context('../attack/techniques/', false, /\.js$/);
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
      this.state['techniques'] = AttackReport.modifyTechniqueData(this.props.report['schema'], this.props.report['techniques']);
    }
  }

  componentDidUpdate(prevProps) {
    if (this.props.report !== prevProps.report) {
     this.setState({schema: this.props.report['schema'],
      techniques: AttackReport.modifyTechniqueData(this.props.report['schema'], this.props.report['techniques'])})
    }
  }

  onTechniqueSelect = (technique, _) => {
    let selectedTechnique = this.getTechniqueByTitle(technique);
    if (selectedTechnique === false){
      return;
    }
    this.setState({selectedTechnique: selectedTechnique.tech_id})
  };

  static getComponentClass(tech_id, techniques) {
    switch (techniques[tech_id].status) {
      case ScanStatus.SCANNED:
        return 'collapse-warning';
      case ScanStatus.USED:
        return 'collapse-danger';
      case ScanStatus.DISABLED:
        return 'collapse-disabled';
      default:
        return 'collapse-default';
    }
  }

  static getStatusIcon(tech_id, techniques){
    switch (techniques[tech_id].status){
      case ScanStatus.SCANNED:
        return <FontAwesomeIcon icon={faEye} className={'technique-status-icon'}/>;
      case ScanStatus.USED:
        return <FontAwesomeIcon icon={faRadiation} className={'technique-status-icon'}/>;
      case ScanStatus.DISABLED:
        return <FontAwesomeIcon icon={faToggleOff} className={'technique-status-icon'}/>;
      default:
        return <FontAwesomeIcon icon={faEyeSlash} className={'technique-status-icon'}/>;
      }
  }

  renderLegend() {
    return (<div id='header' className='row justify-content-between attack-legend'>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className='technique-disabled'/>
        <span> - Disabled</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className='technique-not-attempted'/>
        <span> - Not attempted</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className='technique-attempted'/>
        <span> - Tried (but failed)</span>
      </Col>
      <Col xs={3}>
        <FontAwesomeIcon icon={faCircle} className='technique-used'/>
        <span> - Successfully used</span>
      </Col>
    </div>)
  }

  generateReportContent() {
    return (
        <div>
          <p>
            This report shows information about
            <Button variant={'link'}
                    href={'https://attack.mitre.org/'}
                    size={'lg'}
                    className={'attack-link'}
                    target={'_blank'}>
              Mitre ATT&CK™
            </Button>
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
      if (! Object.prototype.hasOwnProperty.call(this.state.techniques, tech_id)) {return false;}
      let technique = this.state.techniques[tech_id];
      if (technique.title === title){
        technique['tech_id'] = tech_id;
        return technique
      }
    }
    return false;
  }

  static modifyTechniqueData(schema, techniques){
    // add links to techniques
    schema = schema.properties;
    for(const type in schema){
      if (! Object.prototype.hasOwnProperty.call(schema, type)) {return false;}
      let typeTechniques = schema[type].properties;
      for(const tech_id in typeTechniques){
        if (! Object.prototype.hasOwnProperty.call(typeTechniques, tech_id)) {return false;}
        if (typeTechniques[tech_id] !== undefined){
          techniques[tech_id]['link'] = typeTechniques[tech_id].link
        }
      }
    }
    // modify techniques' messages
    for (const tech_id in techniques){
      techniques[tech_id]['message'] = <div dangerouslySetInnerHTML={{__html: marked(techniques[tech_id]['message'])}} />;
    }

    return techniques
  }

  render() {
    let content = {};
    if (typeof this.state.schema === 'undefined' || typeof this.state.techniques === 'undefined') {
      content = <ReportLoader/>;
    } else {
      content = <div> {this.generateReportContent()}</div>;
    }
    return (
    <div id='attack' className='attack-report report-page'>
      <ReportHeader report_type={ReportTypes.attack}/>
      <hr/>
      {content}
     </div>)
  }
}

export default AttackReport;
