import AuthComponent from '../../AuthComponent';
import PillarLabel from './PillarLabel';
import PrinciplesStatusTable from './PrinciplesStatusTable';
import React from 'react';
import * as PropTypes from 'prop-types';
import {Card, Collapse} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faChevronDown} from '@fortawesome/free-solid-svg-icons';
import '../../../styles/pages/report/ZeroTrustReport.scss';

export default class SinglePillarPrinciplesStatus extends AuthComponent {

  constructor(props, context) {
    super(props, context);

    this.state = {
      open: false
    };
  }

  render() {
    const {open} = this.state;
    if (this.props.principlesStatus.length === 0) {
      return null;
    } else {
      return (
        <Card className={'principles-status-card'}>
          <Card.Header onClick={() => this.setState({open: !open})}
                       aria-controls='collapse-content'
                       aria-expanded={open}
                       className={'collapse-control'}>
            <h3 style={{textAlign: 'center', marginTop: '1px', marginBottom: '1px'}}>
              <FontAwesomeIcon icon={faChevronDown}/> <PillarLabel pillar={this.props.pillar}
                                                                   status={this.props.pillarsToStatuses[this.props.pillar]}/>
            </h3>
          </Card.Header>
          <Collapse in={this.state.open}>
            <Card.Body>
              <div id={'collapse-content'}>
                <PrinciplesStatusTable principlesStatus={this.props.principlesStatus}/>
              </div>
            </Card.Body>
          </Collapse>
        </Card>
      );
    }
  }
}

SinglePillarPrinciplesStatus.propTypes = {
  principlesStatus: PropTypes.array,
  pillar: PropTypes.string
};
