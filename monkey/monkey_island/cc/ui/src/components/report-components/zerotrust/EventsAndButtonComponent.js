import React, {Component} from "react";
import EventsModal from "./EventsModal";
import {Button} from "react-bootstrap";
import FileSaver from "file-saver";
import * as PropTypes from "prop-types";
import ExportEventsButton from "./ExportEventsButton";

export default class EventsAndButtonComponent extends Component {
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
          <Button className="btn btn-info" onClick={this.show}>
            Show Events
          </Button>
          <ExportEventsButton onClick={() => {
            const content = JSON.stringify(this.props.events, null, 2);
            const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
            FileSaver.saveAs(blob, this.props.exportFilename + ".json");
          }}/>
        </div>
      </div>
    );
  }

}

EventsAndButtonComponent.propTypes = {
  events: PropTypes.array,
  exportFilename: PropTypes.string,
};
