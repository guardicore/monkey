import React, {Component} from "react";
import {Modal} from "react-bootstrap";
import {EventsTimeline} from "./EventsTimeline";

export class EventsModal extends Component {
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
            </div>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}
