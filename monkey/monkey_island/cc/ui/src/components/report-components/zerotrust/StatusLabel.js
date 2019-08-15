import React, {Component, Fragment} from "react";
import * as PropTypes from "prop-types";

const statusToIcon = {
  "Positive": "fa-check status-success",
  "Inconclusive": "fa-exclamation-triangle status-warning",
  "Conclusive": "fa-bomb status-danger",
  "Unexecuted": "fa-question status-default",
};

export class StatusLabel extends Component {
  render() {
    const classname = "fa " + statusToIcon[this.props.status] + " " + this.props.size;
    let text = "";
    if (this.props.showText) {
      text = " " + this.props.status;
    }
    return (<Fragment>
      <i className={classname}/>{text}
    </Fragment>);
  }
}

StatusLabel.propTypes = {status: PropTypes.string, showText: PropTypes.bool};
