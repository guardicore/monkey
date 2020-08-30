import React from 'react';
import {Modal} from 'react-bootstrap';
import EventsTimeline from './EventsTimeline';
import * as PropTypes from 'prop-types';
import saveJsonToFile from '../../utils/SaveJsonToFile';
import EventsModalButtons from './EventsModalButtons';
import AuthComponent from '../../AuthComponent';
import Pluralize from 'pluralize';
import SkippedEventsTimeline from './SkippedEventsTimeline';

const FINDING_EVENTS_URL = '/api/zero-trust/finding-event/';


export default class EventsModal extends AuthComponent {
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
              There {Pluralize('is', this.props.event_count)} {
                <div className={'badge badge-primary'}>{this.props.event_count}</div>
              } {Pluralize('event', this.props.event_count)} associated with this finding. {
                <div className={'badge badge-primary'}>
                  {this.props.latest_events.length + this.props.oldest_events.length}
                </div>
              } {Pluralize('is', this.props.event_count)} displayed below. All events can be exported using the Export button.
            </p>
            {this.props.event_count > 5 ? this.renderButtons() : null}
            <EventsTimeline events={this.props.oldest_events}/>
            {this.props.event_count > this.props.latest_events.length+this.props.oldest_events.length ?
              this.renderSkippedEventsTimeline() : null}
            <EventsTimeline events={this.props.latest_events}/>
            {this.renderButtons()}
          </Modal.Body>
        </Modal>
      </div>
    );
  }

  renderSkippedEventsTimeline(){
    return <div className={'skipped-events-timeline'}>
      <SkippedEventsTimeline
              skipped_count={this.props.event_count -
                             this.props.latest_events.length + this.props.oldest_events.length}/>
    </div>
  }

  renderButtons() {
    return <EventsModalButtons
      onClickClose={() => this.props.hideCallback()}
      onClickExport={() => {
        let full_url = FINDING_EVENTS_URL + this.props.finding_id;
        this.authFetch(full_url).then(res => res.json()).then(res => {
          const dataToSave = res.events_json;
          const filename = this.props.exportFilename;
          saveJsonToFile(dataToSave, filename);
        });
      }}/>;
  }
}

EventsModal.propTypes = {
  showEvents: PropTypes.bool,
  events: PropTypes.array,
  hideCallback: PropTypes.func
};
