import React, {Component} from "react";
import {Button} from "react-bootstrap";
import * as PropTypes from "prop-types";

export default class PrintReportButton extends Component {
  render() {
    return <div className="text-center no-print">
      <Button bsSize="large" onClick={this.props.onClick}><i className="glyphicon glyphicon-print"/> Print
        Report</Button>
    </div>
  }
}

PrintReportButton.propTypes = {onClick: PropTypes.func};
