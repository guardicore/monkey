import React, {Component} from 'react';
import ExportEventsButton from './ExportEventsButton';
import * as PropTypes from 'prop-types';

export default class EventsModalButtons extends Component {
  render() {
    return <div className="text-center">
      <button type="button" className="btn btn-monkey-info btn-lg" style={{margin: '5px'}}
              onClick={this.props.onClickClose}>
        Close
      </button>
      <ExportEventsButton onClick={this.props.onClickExport}/>
    </div>
  }
}

EventsModalButtons.propTypes = {
  onClickClose: PropTypes.func,
  onClickExport: PropTypes.func
};
