import React, {useState} from 'react';
import {Modal} from 'react-bootstrap';
import * as PropTypes from 'prop-types';
import Pluralize from 'pluralize';
import ScoutSuiteSingleRuleDropdown from './ScoutSuiteSingleRuleDropdown';
import '../../../../styles/components/scoutsuite/RuleModal.scss';
import STATUSES from '../../common/consts/StatusConsts';
import {getRuleCountByStatus, sortRules} from './rule-parsing/ParsingUtils';


export default function ScoutSuiteRuleModal(props) {
  const [openRuleId, setOpenRuleId] = useState(null)

  function toggleRuleDropdown(ruleId) {
    let ruleIdToSet = (openRuleId === ruleId) ? null : ruleId;
    setOpenRuleId(ruleIdToSet);
  }

  function renderRuleDropdowns() {
    let dropdowns = [];
    let rules = sortRules(props.scoutsuite_rules);
    rules.forEach(rule => {
      let dropdown = (<ScoutSuiteSingleRuleDropdown isCollapseOpen={openRuleId === rule.description}
                                                    toggleCallback={() => toggleRuleDropdown(rule.description)}
                                                    rule={rule}
                                                    scoutsuite_data={props.scoutsuite_data}
                                                    key={rule.description + rule.path}/>)
      dropdowns.push(dropdown)
    });
    return dropdowns;
  }

  function getGeneralRuleOverview() {
    return <>
      There {Pluralize('is', props.scoutsuite_rules.length)}
      &nbsp;<span className={'badge badge-primary'}>{props.scoutsuite_rules.length}</span>
      &nbsp;ScoutSuite {Pluralize('rule', props.scoutsuite_rules.length)} associated with this finding.
    </>
  }

  function getFailedRuleOverview() {
    let failedRuleCnt = getRuleCountByStatus(props.scoutsuite_rules, STATUSES.STATUS_FAILED) +
      + getRuleCountByStatus(props.scoutsuite_rules, STATUSES.STATUS_VERIFY);
    return <>
      &nbsp;<span className={'badge badge-danger'}>{failedRuleCnt}</span>
      &nbsp;failed security {Pluralize('rule', failedRuleCnt)}.
    </>
  }

  function getPassedRuleOverview() {
    let passedRuleCnt = getRuleCountByStatus(props.scoutsuite_rules, STATUSES.STATUS_PASSED);
    return <>
      &nbsp;<span className={'badge badge-success'}>{passedRuleCnt}</span>
      &nbsp;passed security {Pluralize('rule', passedRuleCnt)}.
    </>
  }

  function getUnexecutedRuleOverview() {
    let unexecutedRuleCnt = getRuleCountByStatus(props.scoutsuite_rules, STATUSES.STATUS_UNEXECUTED);
    return <>
      &nbsp;<span className={'badge badge-default'}>{unexecutedRuleCnt}</span>
      &nbsp;{Pluralize('rule', unexecutedRuleCnt)} {Pluralize('was', unexecutedRuleCnt)} not
      checked (no relevant resources for the rule).
    </>
  }

  return (
    <div>
      <Modal show={props.isModalOpen} onHide={() => props.hideCallback()} className={'scoutsuite-rule-modal'}>
        <Modal.Body>
          <h3>
            <div className="text-center">ScoutSuite rules</div>
          </h3>
          <hr/>
          <p>
            {getGeneralRuleOverview()}
            {getFailedRuleOverview()}
            {getPassedRuleOverview()}
            {getUnexecutedRuleOverview()}
          </p>
          {renderRuleDropdowns()}
        </Modal.Body>
      </Modal>
    </div>
  );

}

ScoutSuiteRuleModal.propTypes = {
  isModalOpen: PropTypes.bool,
  scoutsuite_rules: PropTypes.array,
  scoutsuite_data: PropTypes.object,
  hideCallback: PropTypes.func
};
