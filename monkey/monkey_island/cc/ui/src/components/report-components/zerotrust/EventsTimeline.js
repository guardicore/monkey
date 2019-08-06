import React, {Component} from "react";
import {Timeline, TimelineEvent} from "react-event-timeline";

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
                icon={<i className="fa fa-circle icon-info" />}>
                  {event.message}
              </TimelineEvent>
            ))
          }
        </Timeline>
      </div>
    );
  }
}
