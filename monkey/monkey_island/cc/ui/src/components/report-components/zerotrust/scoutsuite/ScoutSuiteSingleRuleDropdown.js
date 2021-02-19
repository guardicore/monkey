import React from 'react';
import Collapse from '@kunukn/react-collapse';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faChevronUp} from '@fortawesome/free-solid-svg-icons/faChevronUp'
import {faChevronDown} from '@fortawesome/free-solid-svg-icons/faChevronDown'

import classNames from 'classnames';
import * as PropTypes from 'prop-types';
import STATUSES from '../../common/consts/StatusConsts';
import {faCheckCircle, faCircle, faExclamationCircle} from '@fortawesome/free-solid-svg-icons';
import RuleDisplay from './RuleDisplay';
import {getRuleStatus} from './rule-parsing/ParsingUtils';

export default function ScoutSuiteSingleRuleDropdown(props) {

  function getRuleCollapse() {
    return (
      <div className={classNames('collapse-item',
        'rule-collapse', {'item--active': props.isCollapseOpen})}>
        <button className={classNames('btn-collapse', getDropdownClass())}
                onClick={props.toggleCallback}>
          <span>
            <FontAwesomeIcon icon={getRuleIcon()}/>
            {props.rule.description}
          </span>
          <span>
              <FontAwesomeIcon icon={props.isCollapseOpen ? faChevronDown : faChevronUp}/>
          </span>
        </button>
        <Collapse
          className='collapse-comp'
          isOpen={props.isCollapseOpen}
          render={renderRule}/>
      </div>
    );
  }

  function getRuleIcon() {
    let ruleStatus = getRuleStatus(props.rule);
    switch (ruleStatus) {
      case STATUSES.STATUS_PASSED:
        return faCheckCircle;
      case STATUSES.STATUS_VERIFY:
        return faExclamationCircle;
      case STATUSES.STATUS_FAILED:
        return faExclamationCircle;
      case STATUSES.STATUS_UNEXECUTED:
        return faCircle;
    }
  }

  function getDropdownClass() {
    let ruleStatus = getRuleStatus(props.rule);
    switch (ruleStatus) {
      case STATUSES.STATUS_PASSED:
        return 'collapse-success';
      case STATUSES.STATUS_VERIFY:
        return 'collapse-danger';
      case STATUSES.STATUS_FAILED:
        return 'collapse-danger';
      case STATUSES.STATUS_UNEXECUTED:
        return 'collapse-default';
    }
  }

  function renderRule() {
    return <RuleDisplay rule={props.rule} scoutsuite_data={props.scoutsuite_data}/>
  }

  return getRuleCollapse();
}


ScoutSuiteSingleRuleDropdown.propTypes = {
  isCollapseOpen: PropTypes.bool,
  rule: PropTypes.object,
  scoutsuite_data: PropTypes.object,
  toggleCallback: PropTypes.func
};
