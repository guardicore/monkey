import React, {Component} from "react";
import {Badge, Modal} from "react-bootstrap";
import EventsTimeline from "./EventsTimeline";
import * as PropTypes from "prop-types";
import saveJsonToFile from "../../utils/SaveJsonToFile";
import EventsModalButtons from "./EventsModalButtons";
import Pluralize from 'pluralize'
import {statusToLabelType} from "./StatusLabel";

export default class EventsModal extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Modal show={this.props.showEvents} onHide={() => this.props.hideCallback()}>
          <Modal.Body>
            <h3>
              <div className="text-center">Events</div>
            </h3>
            <hr/>
            <p>
              There {Pluralize('is', this.props.events.length)} {<div
              className={"label label-primary"}>{this.props.events.length}</div>} {Pluralize('event', this.props.events.length)} associated
              with this finding.
            </p>
            {this.props.events.length > 5 ? this.renderButtons() : null}
            <EventsTimeline events={this.props.events}/>
            {this.renderButtons()}
          </Modal.Body>
        </Modal>
      </div>
    );
  }

  renderButtons() {
    return <EventsModalButtons
      onClickClose={() => this.props.hideCallback()}
      onClickExport={() => {
        const dataToSave = this.props.events;
        const filename = this.props.exportFilename;
        saveJsonToFile(dataToSave, filename);
      }}/>;
  }
}

EventsModal.propTypes = {
  showEvents: PropTypes.bool,
  events: PropTypes.array,
  hideCallback: PropTypes.func,
};
