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
    let thead = this.props.thead;

    return(
      <div>
        <table className="table table-condensed">
          {thead}
          <tbody>
          {
            (items.length > this.COLLAPSIBLE_PREVIEW_COUNT) && (!this.state.collapsed) ?
              items.slice(0, this.COLLAPSIBLE_PREVIEW_COUNT).map(parseItemFunction)
              :
              items.map(parseItemFunction)
          }
          </tbody>
          {
            items.length > this.COLLAPSIBLE_PREVIEW_COUNT ?
              <tfoot>
                <tr>
                  <td><Button bsStyle="link" onClick={() => this.setState({'collapsed': !this.state.collapsed})}>
                    See more {this.state.collapsed ? <i className="fa fa-caret-up" /> : <i className="fa fa-caret-down" />}
                  </Button></td>
                </tr>
              </tfoot>
              :
              undefined
          }
        </table>
      </div>
    );
  }
}

export default CollapsedTableComponent;
