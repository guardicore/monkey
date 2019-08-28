import React, {Component} from "react";
import * as PropTypes from "prop-types";

const statusToIcon = {
  "Passed": "fa-check",
  "Inconclusive": "fa-exclamation-triangle",
  "Failed": "fa-bomb",
  "Unexecuted": "fa-question",
};

export const statusToLabelType = {
  "Passed": "label-success",
  "Inconclusive": "label-warning",
  "Failed": "label-danger",
  "Unexecuted": "label-default",
};

export default class StatusLabel extends Component {
  render() {
    let text = "";
    if (this.props.showText) {
      text = " " + this.props.status;
    }

    return (
      <div className={"label " + statusToLabelType[this.props.status]} style={{display: "flow-root"}}>
        <i className={"fa " + statusToIcon[this.props.status] + " " + this.props.size}/>{text}
      </div>
    );
  }
}

StatusLabel.propTypes = {
  status: PropTypes.string,
  showText: PropTypes.bool,
  size: PropTypes.string
};
