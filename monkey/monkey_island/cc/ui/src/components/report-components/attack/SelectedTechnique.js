import React from "react";
import Collapse from '@kunukn/react-collapse';

import AttackReport from '../AttackReport';

const classNames = require('classnames');

class SelectedTechnique extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      techniques: this.props.techniques,
      techComponents: this.props.techComponents,
      selectedTechnique: this.props.selected
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props.selected !== prevProps.selected) {
     this.setState({ selectedTechnique: this.props.selected })
    }
  }

  getSelectedTechniqueComponent(tech_id) {
    const TechniqueComponent = this.state.techComponents[tech_id];
    return (
      <div key={tech_id} className={classNames('collapse-item', {'item--active': true})}>
        <button className={classNames('btn-collapse', AttackReport.getComponentClass(tech_id, this.state.techniques))}>
          <span>{this.state.techniques[tech_id].title}</span>
        </button>
        <Collapse
          className="collapse-comp"
          isOpen={true}
          render={() => {
            return (<div className={`content ${tech_id}`}>
              <TechniqueComponent data={this.state.techniques[tech_id]}/>
            </div>)
          }}/>
      </div>
    );
  }



  render(){
    let content = {};
    let selectedTechId = this.state.selectedTechnique;
    if(selectedTechId === false){
      content = "Select a technique from attack matrix";
    } else {
      content = this.getSelectedTechniqueComponent(selectedTechId)
    }

    return (
      <div>
        <h4 className="selected-technique-title">Selected technique:</h4>
        <section className="attack-report selected-technique">
          {content}
        </section>
      </div>
    )
  }
}

export default SelectedTechnique;
