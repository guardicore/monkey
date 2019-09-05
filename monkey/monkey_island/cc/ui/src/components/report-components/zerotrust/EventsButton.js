import React, {Component, Fragment} from "react";
import EventsModal from "./EventsModal";
import {Badge, Button} from "react-bootstrap";
import * as PropTypes from "prop-types";

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
        <div className="text-center" style={{"display": "grid"}}>
          <Button className="btn btn-primary btn-lg" onClick={this.show}>
            <i className="fa fa-list"/> Events {this.createEventsAmountBadge()}
          </Button>
        </div>
    </Fragment>;
  }

  createEventsAmountBadge() {
    let eventsAmountBadge;
    if (this.props.events.length > 9) {
      eventsAmountBadge = <Badge>9+</Badge>;
    } else {
      eventsAmountBadge = <Badge>{this.props.events.length}</Badge>;
    }
    return eventsAmountBadge;
  }
}

EventsButton.propTypes = {
  events: PropTypes.array,
  exportFilename: PropTypes.string,
};
