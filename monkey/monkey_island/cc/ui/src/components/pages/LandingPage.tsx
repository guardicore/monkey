import React from 'react';
import {Col, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFileCode, faLightbulb} from '@fortawesome/free-solid-svg-icons';
import '../../styles/pages/LandingPage.scss';
import IslandHttpClient from "../IslandHttpClient";


const LandingPageComponent = (props) => {

  return (
    <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
         lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
         className={'landing-page'}>
      <h1 className="page-title">Welcome to the Monkey Island Server</h1>
      <div style={{'fontSize': '1.2em'}}>
        <ScenarioButtons/>
        <br/>
      </div>
    </Col>
  );

  function ScenarioButtons() {
    return (
      <section>
        <h2 className={'scenario-choice-title'}>Choose a scenario:</h2>
        <div className="container">
          <Row className="justify-content-center">
            <div className="col-lg-6 col-sm-6">
              <Link to="/run-monkey"
                    className="px-4 py-5 bg-white shadow text-center d-block"
                    onClick={() => {
                      setScenario('ransomware')
                    }}>
                <h4><FontAwesomeIcon icon={faFileCode}/> Ransomware</h4>
                <p>Simulate ransomware infection in the network.</p>
              </Link>
            </div>
            <div className="col-lg-6 col-sm-6">
              <Link to="/configure"
                    className="px-4 py-5 bg-white shadow text-center d-block"
                    onClick={() => {
                      setScenario('advanced')
                    }}>
                <h4><FontAwesomeIcon icon={faLightbulb}/> Custom</h4>
                <p>Fine tune the simulation to your needs.</p>
              </Link>
            </div>
          </Row>
          <MonkeyInfo/>
        </div>
      </section>
    );
  }

  function setScenario(scenario: string) {
    IslandHttpClient.post('/api/island-mode', {'mode': scenario})
    .then(() => {
      props.onStatusChange();
      });
  }
}

function MonkeyInfo() {
  return (
    <>
      <h4 className={'monkey-description-title'}>What is Infection Monkey?</h4>
      <strong>Infection Monkey</strong> is an open-source security tool for testing a data center's resiliency to
      perimeter
      breaches and internal server infections. The Monkey uses various methods to propagate across a data center
      and reports to this Monkey Island Command and Control server.
    </>
  );
}

export default LandingPageComponent;
