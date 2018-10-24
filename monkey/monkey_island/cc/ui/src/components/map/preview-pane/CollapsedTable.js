import AuthComponent from "../../AuthComponent";
import React from "react";
import {Button} from "react-bootstrap";

class CollapsedTableComponent extends AuthComponent {

  COLLAPSIBLE_PREVIEW_COUNT = 3;

  constructor(props) {
    super(props);
    this.state = {
      collapsed: false
    };
  }

  render() {
    let parseItemFunction = this.props.parseItemFunction;
    let items = this.props.tableItems;

    return(
      <div>
        <table className="table table-condensed"><tbody>
        {items.slice(0, this.COLLAPSIBLE_PREVIEW_COUNT).map(parseItemFunction)}
        {
          items.length > this.COLLAPSIBLE_PREVIEW_COUNT ?
            [<tr><th/><td>
              <Button bsStyle="link" onClick={() => this.setState({'collapsed': !this.state.collapsed})}>
                See more {this.state.collapsed ? <i className="fa fa-caret-up" /> : <i className="fa fa-caret-down" />}
              </Button>
            </td></tr>]
              .concat(
                this.state.collapsed ?
                  items.slice(this.COLLAPSIBLE_PREVIEW_COUNT).map(parseItemFunction)
                  :
                  []
              )
            :
            undefined
        }
        </tbody></table>
      </div>
    );
  }
}

export default CollapsedTableComponent;
