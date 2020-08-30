import React from 'react';
import {Col, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faPlayCircle} from '@fortawesome/free-regular-svg-icons';
import {faBookOpen, faCogs} from '@fortawesome/free-solid-svg-icons';
import '../../styles/pages/RunServerPage.scss';

class RunServerPageComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">Welcome to the Monkey Island Server</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p style={{'marginTop': '30px'}}>
            Congratulations! You have successfully set up the Monkey Island server. &#x1F44F; &#x1F44F;
          </p>
          <br/>
          <HomepageCallToActions />
          <br/>
          <MonkeyInfo />
        </div>
      </Col>
    );
  }
}

export default RunServerPageComponent;

function HomepageCallToActions() {
  return (
    <section id="homepage-shortcuts">
      <div className="container">
        <Row className="justify-content-center">
          <div className="col-lg-4 col-sm-6">
            <Link to="/run-monkey" className="px-4 py-5 bg-white shadow text-center d-block">
              <h4><FontAwesomeIcon icon={faPlayCircle}/> Run Monkey</h4>
              <p>Run the Monkey with the current configuration.</p>
            </Link>
          </div>
          <div className="col-lg-4 col-sm-6">
            <Link to="/configure" className="px-4 py-5 bg-white shadow text-center d-block">
              <h4><FontAwesomeIcon icon={faCogs}/> Configure Monkey</h4>
              <p>Edit targets, add credentials, choose exploits and more.</p>
            </Link>
          </div>
          <div className="col-lg-4 col-sm-6">
            <a href="https://infectionmonkey.com" className="px-4 py-5 bg-white shadow text-center d-block" rel="noopener noreferrer" target="_blank">
              <h4><FontAwesomeIcon icon={faBookOpen}/> Read more</h4>
              <p>Visit our homepage for more information.</p>
            </a>
          </div>
        </Row>
      </div>
    </section>
  );
}

function MonkeyInfo() {
    return (
      <>
        <h4>What is Infection Monkey?</h4>
        <strong>Infection Monkey</strong> is an open-source security tool for testing a data center's resiliency to perimeter
        breaches and internal server infections. The Monkey uses various methods to propagate across a data center
        and reports to this Monkey Island Command and Control server.
      </>
    );
}
