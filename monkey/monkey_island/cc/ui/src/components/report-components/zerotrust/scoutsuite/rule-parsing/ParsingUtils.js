import STATUSES from '../../../common/consts/StatusConsts';
import RULE_LEVELS from '../../../common/consts/ScoutSuiteConsts/RuleLevels';

export function getRuleStatus(rule) {
  if (rule.checked_items === 0) {
    return STATUSES.STATUS_UNEXECUTED
  } else if (rule.items.length === 0) {
    return STATUSES.STATUS_PASSED
  } else if (rule.level === RULE_LEVELS.LEVEL_WARNING) {
    return STATUSES.STATUS_VERIFY
  } else {
    return STATUSES.STATUS_FAILED
  }
}

export function getRuleCountByStatus(rules, status) {
  return rules.filter(rule => getRuleStatus(rule) === status).length;
}

export function sortRules(rules) {
  rules.sort(compareRules);
  return rules;
}

function compareRules(firstRule, secondRule) {
  let firstStatus = getRuleStatus(firstRule);
  let secondStatus = getRuleStatus(secondRule);
  return compareRuleStatuses(firstStatus, secondStatus);
}

function compareRuleStatuses(ruleStatusOne, ruleStatusTwo) {
  const severity_order = {
    [STATUSES.STATUS_FAILED]: 1,
    [STATUSES.STATUS_VERIFY]: 2,
    [STATUSES.STATUS_PASSED]: 3,
    [STATUSES.STATUS_UNEXECUTED]: 4
  }

  return severity_order[ruleStatusOne] - severity_order[ruleStatusTwo]
}
