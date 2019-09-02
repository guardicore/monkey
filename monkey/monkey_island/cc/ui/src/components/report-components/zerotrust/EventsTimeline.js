import React, {Component} from "react";
import {Timeline, TimelineEvent} from "react-event-timeline";
import * as PropTypes from "prop-types";

let monkeyLocalIcon = require('../../../images/zerotrust/im-alert-machine-icon.svg');
let monkeyNetworkIcon = require('../../../images/zerotrust/im-alert-network-icon.svg');

const eventTypeToIcon = {
  "monkey_local": monkeyLocalIcon,
  "monkey_network": monkeyNetworkIcon,
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
                icon={<img src={eventTypeToIcon[event.event_type]} alt="icon" style={{width: '24px'}} />}>
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
