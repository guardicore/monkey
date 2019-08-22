import React, {Component} from "react";
import {Timeline, TimelineEvent} from "react-event-timeline";
import * as PropTypes from "prop-types";

const eventTypeToIcon = {
  "monkey_local": "fa fa-exclamation-circle fa-2x icon-warning",
  "monkey_network": "fa fa-exclamation-circle fa-2x icon-warning",
  "island": "fa fa-server fa-2x icon-info",
  null: "fa fa-question-circle fa-2x icon-info",
};

export default class EventsTimeline extends Component {
  render() {
    return (
      <div>
        <Timeline>
          {
            this.props.events.map((event, index) => {
              const event_time = new Date(event.timestamp['$date']).toString();
              return (<TimelineEvent
                key={index}
                createdAt={event_time}
                title={event.title}
                icon={<i className={eventTypeToIcon[event.event_type]} />}>
                  {event.message}
              </TimelineEvent>)
            })
          }
        </Timeline>
      </div>
    );
  }
}

EventsTimeline.propTypes = {events: PropTypes.array};
