import React from 'react';
import Collapse from '@kunukn/react-collapse';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons/faQuestionCircle'
import { faChevronUp } from '@fortawesome/free-solid-svg-icons/faChevronUp'
import { faChevronDown } from '@fortawesome/free-solid-svg-icons/faChevronDown'
import { faToggleOn } from '@fortawesome/free-solid-svg-icons/faToggleOn'

import {Button} from 'react-bootstrap';
import AttackReport from '../AttackReport';

import classNames from 'classnames';

class TechniqueDropdowns extends React.Component{

  constructor(props) {
    super(props);
    this.state = {
      techniques: this.props.techniques,
      techComponents: this.props.techComponents,
      schema: this.props.schema,
      collapseOpen: '',
      techniquesHidden: true
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props.techniques !== prevProps.techniques) {
     this.setState({ techniques: this.props.techniques })
    }
  }

  onToggle = technique =>
    this.setState(state => ({collapseOpen: state.collapseOpen === technique ? null : technique}));

  getTechniqueCollapse(tech_id) {
    return (
      <div key={tech_id} className={classNames('collapse-item', {'item--active': this.state.collapseOpen === tech_id})}>
        <button className={classNames('btn-collapse', AttackReport.getComponentClass(tech_id, this.state.techniques))}
                onClick={() => this.onToggle(tech_id)}>
          <span>
            {AttackReport.getStatusIcon(tech_id, this.state.techniques)}
            {this.state.techniques[tech_id].title}
          </span>
          <span>
            <a href={this.state.techniques[tech_id].link} rel="noopener noreferrer" target='_blank'>
              <FontAwesomeIcon icon={faQuestionCircle} className={'link-to-technique'}
                               color={AttackReport.getComponentClass(tech_id, this.state.techniques) === 'collapse-default' ? '#ffffff' : '#000000'}/>
            </a>
              <FontAwesomeIcon icon={this.state.collapseOpen === tech_id ? faChevronDown : faChevronUp}/>
          </span>
        </button>
        <Collapse
          className='collapse-comp'
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
    const TechniqueComponent = this.state.techComponents[technique];
    return (
      <div className={`content ${collapseState}`}>
        <TechniqueComponent data={this.state.techniques[technique]}/>
      </div>
    );
  }

  toggleTechList(){
    this.setState({techniquesHidden: (! this.state.techniquesHidden)})
  }

  getOrderedTechniqueList(){
    let content = [];
    for(const type_key in this.state.schema.properties){
      if (! Object.prototype.hasOwnProperty.call(this.state.schema.properties, type_key)){
        continue;
      }
      let tech_type = this.state.schema.properties[type_key];
      content.push(<h3>{tech_type.title}</h3>);
      for(const tech_id in this.state.techniques){
        if (! Object.prototype.hasOwnProperty.call(this.state.techniques, tech_id)){
          continue;
        }
        let technique = this.state.techniques[tech_id];
        if(technique.type === tech_type.title){
          content.push(this.getTechniqueCollapse(tech_id))
        }
      }
    }
    return content
  }

  render(){
    let content = [];
    let listClass = '';
    if (this.state.techniquesHidden){
      listClass = 'hidden-list'
    } else {
      content = this.getOrderedTechniqueList()
    }
    return (
      <div className='attack-technique-list-component'>
        <h3>
          List of all techniques
          <Button variant='link'
                  size='lg'
                  onClick={() => this.toggleTechList()}
                  className={classNames({'toggle-btn': true,
                                         'toggled-off' : this.state.techniquesHidden,
                                         'toggled-on': !this.state.techniquesHidden})}>
            <FontAwesomeIcon icon={faToggleOn} className={'switch-on'} size={'2x'}/>
            <FontAwesomeIcon icon={faToggleOn} className={'switch-off'} size={'2x'}/>
          </Button>
        </h3>
        <section className={`dropdown-list ${listClass}`}>{content}</section>
      </div>);
  }
}

export default TechniqueDropdowns;
