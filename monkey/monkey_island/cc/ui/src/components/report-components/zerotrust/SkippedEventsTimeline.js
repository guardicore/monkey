import React, {Component} from 'react';
import {Timeline, TimelineEvent} from 'react-event-timeline';
import { faArrowsAltV } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as PropTypes from 'prop-types';


export default class SkippedEventsTimeline extends Component {

  render() {
    return (
      <div>
        <Timeline style={{fontSize: '100%'}}>
          <TimelineEvent
            bubbleStyle={{border: '2px solid #ffcc00'}}
            title='Events in between are not displayed, but can be exported to JSON.'
            icon={<FontAwesomeIcon className={'timeline-event-icon'} icon={faArrowsAltV}/>} >
            {this.props.skipped_count} events not displayed.
          </TimelineEvent>
        </Timeline>
      </div>
    );
  }
}

SkippedEventsTimeline.propTypes = {skipped_count: PropTypes.number};
