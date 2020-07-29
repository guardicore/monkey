import React, {Component} from 'react';
import StatusLabel from './StatusLabel';
import {ZeroTrustStatuses} from './ZeroTrustPillars';
import {NavLink} from 'react-router-dom';
import {Card, Collapse} from 'react-bootstrap';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faChevronDown} from '@fortawesome/free-solid-svg-icons/faChevronDown';


class ZeroTrustReportLegend extends Component {

  constructor(props, context) {
    super(props, context);

    this.state = {
      open: false
    };
  }

  render() {
    const legendContent = this.getLegendContent();
    const {open} = this.state;

    return (
      <Card>
        <Card.Header onClick={() => this.setState({open: !open})}
                  aria-controls='collapse-content'
                  aria-expanded={open}
                  className={'collapse-control'}>
            <h3><FontAwesomeIcon icon={faChevronDown}/> Legend</h3>
        </Card.Header>

        <Collapse in={this.state.open}>
          <Card.Body>
            <div id='collapse-content'>
              {legendContent}
            </div>
          </Card.Body>
        </Collapse>
      </Card>
    );
  }

  getLegendContent() {
    return <div id={this.constructor.name}>
      <ul style={{listStyle: 'none'}}>
        <li>
          <div style={{display: 'inline-block'}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.failed}/>
          </div>
          {'\t'}At least one of the tests related to this component failed. This means that the Infection Monkey
          detected an
          unmet Zero Trust requirement.
        </li>
        <li>
          <div style={{display: 'inline-block'}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.verify}/>
          </div>
          {'\t'}At least one of the tests’ results related to this component requires further manual verification.
        </li>
        <li>
          <div style={{display: 'inline-block'}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.passed}/>
          </div>
          {'\t'}All Tests related to this pillar passed. No violation of a Zero Trust guiding principle was detected.
        </li>
        <li>
          <div style={{display: 'inline-block'}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.unexecuted}/>
          </div>
          {'\t'}This status means the test wasn't executed.To activate more tests, refer to the Monkey <NavLink
          to="/configure"><u>configuration</u></NavLink> page.
        </li>
      </ul>
    </div>;
  }
}

export default ZeroTrustReportLegend;
