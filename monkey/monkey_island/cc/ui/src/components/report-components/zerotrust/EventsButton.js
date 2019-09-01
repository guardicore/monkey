import React, {Component} from "react";
import EventsModal from "./EventsModal";
import {Button} from "react-bootstrap";
import FileSaver from "file-saver";
import * as PropTypes from "prop-types";
import ExportEventsButton from "./ExportEventsButton";

export default class EventsButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShow: false
    }
  }

  hide = () => {
    this.setState({isShow: false});
  };

  show = () => {
    this.setState({isShow: true});
  };

  render() {
    return (
      <div>
        <EventsModal events={this.props.events} showEvents={this.state.isShow} hideCallback={this.hide} exportFilename={this.props.exportFilename} />
        <div className="text-center" style={{"display": "grid"}}>
          <Button className="btn btn-primary btn-lg" onClick={this.show}>
            <i className="fa fa-list"/> Events
          </Button>
        </div>
      </div>
    );
  }

}

EventsButton.propTypes = {
  events: PropTypes.array,
  exportFilename: PropTypes.string,
};
