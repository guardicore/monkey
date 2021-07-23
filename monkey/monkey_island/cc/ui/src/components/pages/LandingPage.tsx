import React from 'react';
import {Col, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons';
import {faFileCode, faLightbulb} from '@fortawesome/free-solid-svg-icons';
import '../../styles/pages/LandingPage.scss';
import IslandHttpClient from "../IslandHttpClient";
import VersionComponent from '../side-menu/VersionComponent';
import {Routes} from "../Main";

const guardicoreLogoImage = require('../../images/guardicore-logo.png');

const LandingPageComponent = (props) => {

  return (
  <>
    <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
         lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
         className={'landing-page'}>
        <h1 className="page-title">Breach & Attack Simulation</h1>
        <div style={{'fontSize': '1.2em'}}>
          <ScenarioButtons/>
        <br/>
      </div>
    </Col>

    <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
         lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
         className={'guardicore-logo'}>
         <hr/>
        <GuardicoreLogo/>
    </Col>
  </>
  );


  function ScenarioButtons() {
    return (
      <section>
        <h2 className={'scenario-choice-title'}>Choose a scenario:</h2>
        <div className="container">
          <ScenarioInfo/>
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

function ScenarioInfo() {
    // TODO change links when added to documentation
    return (
      <>
        <div className={'scenario-info'}>
          Check monkey documentation hub for better explanation
          on <a href='https://www.guardicore.com/infectionmonkey/docs' rel="noopener noreferrer" target="_blank">
           Ransomware
          </a> and <a href='https://www.guardicore.com/infectionmonkey/docs' rel="noopener noreferrer" target="_blank">
           Custom
          </a> simulations.
        </div>
      </>
    );
}

function GuardicoreLogo() {
  return (
    <>
      <div className='guardicore-link text-center' style={{'marginBottom': '0.5em'}}>
        <span>Powered by</span>
        <a href='http://www.guardicore.com' rel='noopener noreferrer' target='_blank'>
          <img src={guardicoreLogoImage} alt='GuardiCore'/>
        </a>
      </div>
      <div className='license-link text-center'>
        <a href='https://www.guardicore.com/infectionmonkey/docs' rel="noopener noreferrer" target="_blank">
          <FontAwesomeIcon icon={faExternalLinkAlt} /> Documentation
        </a>
        <br/>
        <Link to={Routes.LicensePage}>License</Link>
      </div>
      <VersionComponent/>
    </>
  );
}

export default LandingPageComponent;
