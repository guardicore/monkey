import React, {Component} from 'react';
import {Button} from 'react-bootstrap';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload';

export default class ExportEventsButton extends Component {
  render() {
    return <Button className="btn btn-primary btn-lg"
                   onClick={this.props.onClick}
    >
      <FontAwesomeIcon icon={faDownload}/> Export
    </Button>
  }
}

ExportEventsButton.propTypes = {onClick: PropTypes.func};
