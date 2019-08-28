import React, {Component} from "react";
import {Button} from "react-bootstrap";
import * as PropTypes from "prop-types";

export default class ExportEventsButton extends Component {
  render() {
    return <Button className="btn btn-primary"
                   onClick={this.props.onClick}
    >
      Export Events
    </Button>
  }
}

ExportEventsButton.propTypes = {onClick: PropTypes.func};
