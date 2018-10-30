import AuthComponent from "../../AuthComponent";
import React from "react";
import {Button, PanelGroup} from "react-bootstrap";

class CollapsedPanelGroupComponent extends AuthComponent {

  COLLAPSIBLE_PREVIEW_COUNT = 3;

  constructor(props) {
    super(props);
    this.state = {
      collapsed: false
    };
  }

  render() {
    let parseItemFunction = this.props.parseItemFunction;
    let items = this.props.panelItems;
    let id = this.props.id;

    return(
      <div>
        <PanelGroup
          accordion
          id={id}>
          {
            (items.length > this.COLLAPSIBLE_PREVIEW_COUNT) && (!this.state.collapsed) ?
              items.slice(0, this.COLLAPSIBLE_PREVIEW_COUNT).map(parseItemFunction)
              :
              items.map(parseItemFunction)
          }
        </PanelGroup>
        {
          items.length > this.COLLAPSIBLE_PREVIEW_COUNT ?
            <Button bsStyle="link" onClick={() => this.setState({'collapsed': !this.state.collapsed})}>
              See more {this.state.collapsed ? <i className="fa fa-caret-up" /> : <i className="fa fa-caret-down" />}
            </Button>
            :
            undefined
        }
      </div>
    );
  }
}

export default CollapsedPanelGroupComponent;
