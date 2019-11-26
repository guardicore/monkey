import React from "react";
import Collapse from '@kunukn/react-collapse';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle, faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons'

import {Button} from 'react-bootstrap';
import AttackReport from '../AttackReport';

const classNames = require('classnames');

class TechniqueDropdowns extends React.Component{

  constructor(props) {
    super(props);
    this.state = {
      techniques: this.props.techniques,
      techComponents: this.props.techComponents,
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
          <span>{this.state.techniques[tech_id].title}</span>
          <span>
            <a href={this.state.techniques[tech_id].link} target="_blank">
              <FontAwesomeIcon icon={faQuestionCircle}/>
            </a>
              <FontAwesomeIcon icon={this.state.collapseOpen === tech_id ? faChevronDown : faChevronUp}/>
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

  render(){
    let listClass = '';
    let content = [];
    if (this.state.techniquesHidden){
      listClass = "hidden-list"
    } else {
      Object.keys(this.state.techniques).forEach((tech_id) => {
        content.push(this.getTechniqueCollapse(tech_id))
      });
    }
    return (
      <div className="dropdown-list">
        <Button bsStyle="link"
                bsSize="large"
                onClick={() => this.toggleTechList()}>
          {this.state.techniquesHidden ? "Show all" : "Hide all"}
        </Button>
        <section className={`attack-report ${listClass}`}>{content}</section>
      </div>);
  }
}

export default TechniqueDropdowns;
