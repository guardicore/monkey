import React, {Component, Fragment} from 'react';
import EventsModal from './EventsModal';
import {Badge, Button} from 'react-bootstrap';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faList } from '@fortawesome/free-solid-svg-icons/faList';

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
      <EventsModal events={this.props.events} showEvents={this.state.isShow} hideCallback={this.hide}
                   exportFilename={this.props.exportFilename}/>
      <div className="text-center" style={{'display': 'grid'}}>
        <Button className="btn btn-primary btn-lg" onClick={this.show}>
          <FontAwesomeIcon icon={faList}/> Events {this.createEventsAmountBadge()}
        </Button>
      </div>
    </Fragment>;
  }

  createEventsAmountBadge() {
    const eventsAmountBadgeContent = this.props.events.length > 9 ? '9+' : this.props.events.length;
    return <Badge>{eventsAmountBadgeContent}</Badge>;
  }
}

EventsButton.propTypes = {
  events: PropTypes.array,
  exportFilename: PropTypes.string
};
