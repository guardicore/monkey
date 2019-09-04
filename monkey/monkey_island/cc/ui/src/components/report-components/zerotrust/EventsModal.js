import React, {Component} from "react";
import {Modal} from "react-bootstrap";
import EventsTimeline from "./EventsTimeline";
import * as PropTypes from "prop-types";
import ExportEventsButton from "./ExportEventsButton";
import saveJsonToFile from "../../utils/SaveJsonToFile";

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
                const dataToSave = this.props.events;
                const filename = this.props.exportFilename;
                saveJsonToFile(dataToSave, filename);
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
