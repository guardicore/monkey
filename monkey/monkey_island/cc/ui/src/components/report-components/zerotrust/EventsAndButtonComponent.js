import React, {Component} from "react";
import EventsModal from "./EventsModal";
import {Button} from "react-bootstrap";
import FileSaver from "file-saver";
import * as PropTypes from "prop-types";

export default class EventsAndButtonComponent extends Component {
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
    return (
      <div>
        <EventsModal events={this.props.events} showEvents={this.state.isShow} hideCallback={this.hide}/>
        <p style={{margin: '1px'}}>
          <Button className="btn btn-info btn-lg center-block"
                  onClick={this.show}>
            Show Events
          </Button>
          <Button className="btn btn-primary btn-lg center-block"
                  onClick={() => {
                    const content = JSON.stringify(this.props.events, null, 2);
                    const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
                    FileSaver.saveAs(blob, this.props.exportFilename + ".json");
                  }}
          >
            Export Events
          </Button>
        </p>
      </div>
    );
  }

}

EventsAndButtonComponent.propTypes = {
  events: PropTypes.array,
  exportFilename: PropTypes.string,
};
