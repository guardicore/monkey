import { Badge } from "react-bootstrap";
import React from "react";

function CountBadge(props) {
  const TEXT_FOR_LARGE_RULE_COUNT = props.maxCount + "+";

  const ruleCountText =
    props.count > props.maxCount ? TEXT_FOR_LARGE_RULE_COUNT : props.count;

  return <Badge variant={"monkey-info-light"}>{ruleCountText}</Badge>;
}

CountBadge.defaultProps = {
  maxCount: 9,
};

export default CountBadge;
