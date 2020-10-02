import React from 'react';
import * as PropTypes from 'prop-types';
import '../../../../styles/components/scoutsuite/RuleDisplay.scss'
import ResourceDropdown from './ResourceDropdown';

export default function RuleDisplay(props) {

  return (
    <div className={'scoutsuite-rule-display'}>
      <div className={'description'}>
        <h3>{props.rule.description}({props.rule.service})</h3>
      </div>
      <div className={'rationale'}>
        <p dangerouslySetInnerHTML={{__html: props.rule.rationale}} />
      </div>
      <div className={'checked-resources'}>
        <p className={'checked-resources-title'}>Resources checked: </p>
        <p>{props.rule.checked_items}</p>
      </div>
      <div className={'flagged-resources'}>
        <p className={'checked-resources-title'}>Resources flagged: </p>
        <p>{props.rule.flagged_items}</p>
      </div>
      {props.rule.references.length !== 0 ? getReferences() : ''}
      {props.rule.items.length !== 0 ? getResources() : ''}
    </div>);

  function getReferences() {
    let references = []
    props.rule.references.forEach(reference => {
      references.push(<a href={reference} className={'reference-link'} target={'_blank'}>{reference}</a>)
    })
    return (
      <div className={'reference-list'}>
        <p className={'reference-list-title'}>References:</p>
        {references}
      </div>)
  }

  function getResources() {
    let resources = []
    props.rule.items.forEach(item => {
      let template_path = props.rule.hasOwnProperty('display_path') ? props.rule.display_path : props.rule.path;
      resources.push(<ResourceDropdown resource_path={item}
                                       template_path={template_path}
                                       scoutsuite_data={props.scoutsuite_data}/>)
    })
    return (
      <div className={'reference-list'}>
        <p className={'reference-list-title'}>Resources:</p>
        {resources}
      </div>)
  }
}

RuleDisplay.propTypes = {
  rule: PropTypes.object,
  scoutsuite_data: PropTypes.object
};
