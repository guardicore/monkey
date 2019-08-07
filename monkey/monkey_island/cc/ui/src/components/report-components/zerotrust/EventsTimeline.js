import React, {Component} from "react";
import {Timeline, TimelineEvent} from "react-event-timeline";

const eventTypeToIcon = {
  "MonkeyAction": "fa fa-exclamation-circle fa-2x icon-warning",
  "IslandAction": "fa fa-server fa-2x icon-info",
  null: "fa fa-question-circle fa-2x icon-info",
};

export class EventsTimeline extends Component {
  render() {
    return (
      <div>
        <Timeline>
          {
            this.props["events"].map(event => (
              <TimelineEvent
                key={event.timestamp}
                createdAt={event.timestamp}
                title={event.title}
                icon={<i className={eventTypeToIcon[event.type]} />}>
                  {event.message}
              </TimelineEvent>
            ))
          }
        </Timeline>
      </div>
    );
  }
}
