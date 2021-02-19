import React, {Component, Fragment} from 'react';
import EventsModal from './EventsModal';
import {Button} from 'react-bootstrap';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faList } from '@fortawesome/free-solid-svg-icons/faList';
import CountBadge from '../../ui-components/CountBadge';

export default class EventsButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShow: false
    }
  }

  hide = () => {
    this.setState({isShow: false});
  };

  show = () => {
    this.setState({isShow: true});
  };

  render() {
    return <Fragment>
      <EventsModal finding_id={this.props.finding_id}
                   latest_events={this.props.latest_events}
                   oldest_events={this.props.oldest_events}
                   event_count={this.props.event_count}
                   showEvents={this.state.isShow}
                   hideCallback={this.hide}
                   exportFilename={this.props.exportFilename}/>
      <div className="text-center" style={{'display': 'grid'}}>
        <Button variant={'monkey-info'} size={'lg'} onClick={this.show}>
          <FontAwesomeIcon icon={faList}/> Events <CountBadge count={this.props.event_count} />
        </Button>
      </div>
    </Fragment>;
  }
}

EventsButton.propTypes = {
  latest_events: PropTypes.array,
  oldest_events: PropTypes.array,
  event_count: PropTypes.number,
  exportFilename: PropTypes.string
};
