import React from 'react';
import {NavLink, Route, BrowserRouter as Router} from 'react-router-dom';
import {Col, Grid, Row} from 'react-bootstrap';
import {Icon} from 'react-fa';

import RunServerPage from 'components/pages/RunServerPage';
import ConfigurePage from 'components/pages/ConfigurePage';
import RunMonkeyPage from 'components/pages/RunMonkeyPage';
import MapPage from 'components/pages/MapPage';
import FullLogsPage from 'components/pages/FullLogsPage';

require('normalize.css/normalize.css');
require('react-data-components/css/table-twbs.css');
require('styles/App.css');

let logoImage = require('../images/monkey-logo.png');
let guardicoreLogoImage = require('../images/guardicore-logo.png');

class AppComponent extends React.Component {
  render() {
    return (
      <Router>
        <Grid fluid={true}>
          <Row>
            <Col sm={3} md={2} className="sidebar">
              <div className="header">
                <img src={logoImage} alt="Infection Monkey"/>
              </div>

              <ul className="navigation">
                <li>
                  <NavLink to="/" exact={true}>
                    <span className="number">1.</span>
                    Run C&C Server
                    <Icon name="check" className="pull-right checkmark text-success"/>
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/run-monkey">
                    <span className="number">2.</span>
                    Run Monkey
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/infection/map">
                    <span className="number">3.</span>
                    Infection Map
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/report">
                    <span className="number">4.</span>
                    Pen. Test Report
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/start-over">
                    <span className="number">5.</span>
                    Start Over
                  </NavLink>
                </li>
              </ul>

              <hr/>
              <ul>
                <li><NavLink to="/configure">Configuration</NavLink></li>
                <li><NavLink to="/infection/logs">Monkey Telemetry</NavLink></li>
              </ul>

              <hr/>
              <div className="guardicore-link">
                <span>Powered by</span>
                <a href="http://www.guardicore.com" target="_blank">
                  <img src={guardicoreLogoImage} alt="GuardiCore"/>
                </a>
              </div>

            </Col>
            <Col sm={9} md={10} smOffset={3} mdOffset={2} className="main">
              <Route exact path="/" component={RunServerPage}/>
              <Route path="/configure" component={ConfigurePage}/>
              <Route path="/run-monkey" component={RunMonkeyPage}/>
              <Route path="/infection/map" component={MapPage}/>
              <Route path="/infection/logs" component={FullLogsPage}/>
              {/*<Route path="/report" component={ReportPage}/>*/}
            </Col>
          </Row>
        </Grid>
      </Router>
    );
  }
}

AppComponent.defaultProps = {};

export default AppComponent;
