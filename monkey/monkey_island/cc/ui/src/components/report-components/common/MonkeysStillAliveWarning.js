import React, {Component} from "react";
import * as PropTypes from "prop-types";

export class MonkeysStillAliveWarning extends Component {
  render() {
    return <div>
      {
        this.props.allMonkeysAreDead ?
          ''
          :
          (<p className="alert alert-warning">
            <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
            Some monkeys are still running. To get the best report it's best to wait for all of them to finish
            running.
          </p>)
      }
    </div>
  }
}

MonkeysStillAliveWarning.propTypes = {allMonkeysAreDead: PropTypes.bool};
