import React from 'react';
import {Col, Row} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFileCode, faLightbulb} from '@fortawesome/free-solid-svg-icons';
import '../../styles/pages/LandingPage.scss';
import IslandHttpClient from "../IslandHttpClient";

import ParticleBackground from '../ui-components/ParticleBackground';
import Logo from "../logo/LogoComponent";

const monkeyIcon = require('../../images/monkey-icon.svg')
const infectionMonkey = require('../../images/infection-monkey.svg')

type Props = {
  onStatusChange: () => void
}

const LandingPageComponent = (props: Props) => {
  return (
    <>
      <ParticleBackground/>
      <Col sm={{offset: 1, span: 10}} md={{offset: 1, span: 10}}
           lg={{offset: 2, span: 8}} xl={{offset: 3, span: 6}}
           className={'landing-page'}>
        <MonkeyBanner/>
        <div className={'scenario-header'}>
          <ScenarioButtons/>
          <br/>
          <Col className={'guardicore-logo'}>
            <Logo/>
          </Col>
        </div>
        <br/>
        <br/>
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
    IslandHttpClient.put('/api/island/mode',  scenario)
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
  return (
    <>
      <div className={'scenario-info'}>
        Check the Infection Monkey documentation hub for more information
        on <a href='https://techdocs.akamai.com/infection-monkey/docs/scenarios' rel="noopener noreferrer"
              target="_blank">
        scenarios
      </a>.
      </div>
    </>
  );
}

function MonkeyBanner(props) {
  return (
    <div className={'landing-page-banner'}>
      <img className={'landing-banner-component landing-banner-monkey-icon'} src={monkeyIcon}/>
      <img className={'landing-banner-component landing-banner-title'} src={infectionMonkey}/>
    </div>
  );
}

export default LandingPageComponent;
