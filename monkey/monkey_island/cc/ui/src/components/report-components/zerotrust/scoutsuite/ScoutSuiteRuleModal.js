import React, {useState} from 'react';
import {Modal} from 'react-bootstrap';
import * as PropTypes from 'prop-types';
import Pluralize from 'pluralize';
import ScoutSuiteSingleRuleDropdown from './ScoutSuiteSingleRuleDropdown';
import '../../../../styles/components/scoutsuite/RuleModal.scss';


export default function ScoutSuiteRuleModal(props) {
  const [openRuleId, setOpenRuleId] = useState(null)

  function toggleRuleDropdown(ruleId) {
    if (openRuleId === ruleId) {
      setOpenRuleId(null);
    } else {
      setOpenRuleId(ruleId);
    }
  }

  function renderRuleDropdowns() {
    let dropdowns = [];
    props.scoutsuite_rules.forEach(rule => {
      let dropdown = (<ScoutSuiteSingleRuleDropdown isCollapseOpen={openRuleId === rule.description}
                                                    toggleCallback={() => toggleRuleDropdown(rule.description)}
                                                    rule={rule}
                                                    scoutsuite_data={props.scoutsuite_data}/>)
      dropdowns.push(dropdown)
    });
    return dropdowns;
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
            There {Pluralize('is', props.scoutsuite_rules.length)} {
            <div className={'badge badge-primary'}>{props.scoutsuite_rules.length}</div>
          } ScoutSuite {Pluralize('rule', props.scoutsuite_rules.length)} associated with finding.
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
