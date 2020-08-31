import React, {Component} from 'react';
import {Button} from 'react-bootstrap';
import * as PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPrint } from '@fortawesome/free-solid-svg-icons/faPrint';

export default class PrintReportButton extends Component {
  render() {
    return <div className="text-center no-print">
      <Button size="md" variant={'outline-standard'} onClick={this.props.onClick}>
        <FontAwesomeIcon icon={faPrint}/> Print
        Report</Button>
    </div>
  }
}

PrintReportButton.propTypes = {onClick: PropTypes.func};
