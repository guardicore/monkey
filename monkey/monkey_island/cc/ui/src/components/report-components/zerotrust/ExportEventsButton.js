import React, {Component} from "react";
import {Button} from "react-bootstrap";
import * as PropTypes from "prop-types";

export default class ExportEventsButton extends Component {
  render() {
    return <Button className="btn btn-primary btn-lg"
                   onClick={this.props.onClick}
    >
      <i className="fa fa-download"/> Export
    </Button>
  }
}

ExportEventsButton.propTypes = {onClick: PropTypes.func};
