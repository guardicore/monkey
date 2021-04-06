import React from 'react';
import {Col} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import AuthComponent from '../../AuthComponent';
import RunOptions from './RunOptions';


class RunMonkeyPageComponent extends AuthComponent {

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">1. Run Monkey</h1>
        <p style={{'marginBottom': '2em', 'fontSize': '1.2em'}}>
          Go ahead and run the monkey!
          <i> (Or <Link to="/configure">configure the monkey</Link> to fine tune its behavior)</i>
        </p>
        <RunOptions />
      </Col>
    );
  }
}

export default RunMonkeyPageComponent;
