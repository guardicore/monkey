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

class AppComponent extends React.Component {
  render() {
    return (
      <Router>
        <Grid fluid={true}>
          <Row>
            <Col sm={3} md={2} className="sidebar">
              <div className="header">
                <img src={logoImage} alt="Infection Monkey"/>
                by GuardiCore
              </div>

              <ul className="navigation">
                <li>
                  <NavLink to="/" exact={true}>
                    <span className="number">1.</span>
                    Run Server
                    <Icon name="check" className="pull-right checkmark text-success"/>
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/configure">
                    <span className="number">2.</span>
                    Configure
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/run-monkey">
                    <span className="number">3.</span>
                    Run Monkey
                  </NavLink>
                </li>
                <li>
                  <a className="disabled">
                    <span className="number">4.</span>
                    Infection
                  </a>
                  <ul>
                    <li><NavLink to="/infection/map">Map</NavLink></li>
                    <li><NavLink to="/infection/logs">Full Logs</NavLink></li>
                  </ul>
                </li>
                <li>
                  <NavLink to="/report">
                    <span className="number">5.</span>
                    Pen. Test Report
                  </NavLink>
                </li>
              </ul>

              <hr/>
              <ul>
                <li><a>Clear DB</a></li>
                <li><a>Kill All Monkeys</a></li>
              </ul>
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
