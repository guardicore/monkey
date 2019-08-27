import React, {Component} from "react";
import {Modal} from "react-bootstrap";
import EventsTimeline from "./EventsTimeline";
import * as PropTypes from "prop-types";
import FileSaver from "file-saver";
import ExportEventsButton from "./ExportEventsButton";

export default class EventsModal extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Modal show={this.props.showEvents} onHide={() => this.props.hideCallback()}>
          <Modal.Body>
            <h2>
              <div className="text-center">Events</div>
            </h2>

            <EventsTimeline events={this.props.events}/>

            <div className="text-center">
              <button type="button" className="btn btn-success btn-lg" style={{margin: '5px'}}
                      onClick={() => this.props.hideCallback()}>
                Close
              </button>
              <ExportEventsButton onClick={() => {
                const content = JSON.stringify(this.props.events, null, 2);
                const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
                FileSaver.saveAs(blob, this.props.exportFilename + ".json");
              }}/>
            </div>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}

EventsModal.propTypes = {
  showEvents: PropTypes.bool,
  events: PropTypes.array,
  hideCallback: PropTypes.func,
};
