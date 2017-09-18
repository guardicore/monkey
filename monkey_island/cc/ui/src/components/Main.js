import React from 'react';
import {NavLink, Route, BrowserRouter as Router} from 'react-router-dom';
import {Col, Grid, Row} from 'react-bootstrap';
import {Icon} from 'react-fa';

import RunServerPage from 'components/pages/RunServerPage';
import ConfigurePage from 'components/pages/ConfigurePage';
import RunMonkeyPage from 'components/pages/RunMonkeyPage';
import MapPage from 'components/pages/MapPage';
import FullLogsPage from 'components/pages/FullLogsPage';
import StartOverPage from 'components/pages/StartOverPage';
import ReportPage from 'components/pages/ReportPage';

require('normalize.css/normalize.css');
require('react-data-components/css/table-twbs.css');
require('styles/App.css');

let logoImage = require('../images/monkey-logo.png');
let guardicoreLogoImage = require('../images/guardicore-logo.png');

class AppComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      completedSteps: {
        run_server: true,
        run_monkey: false,
        infection_done: false
      }
    };
  }
  updateStatus = () => {
    fetch('/api')
      .then(res => res.json())
      .then(res => this.setState({completedSteps: res['completed_steps']}));
  }

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
                    { this.state.completedSteps.run_server ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/run-monkey">
                    <span className="number">2.</span>
                    Run Monkey
                    { this.state.completedSteps.run_monkey ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/infection/map">
                    <span className="number">3.</span>
                    Infection Map
                    { this.state.completedSteps.infection_done ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
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
              <div className="guardicore-link text-center">
                <span>Powered by</span>
                <a href="http://www.guardicore.com" target="_blank">
                  <img src={guardicoreLogoImage} alt="GuardiCore"/>
                </a>
              </div>

            </Col>
            <Col sm={9} md={10} smOffset={3} mdOffset={2} className="main">
              <Route exact path="/" render={(props) => ( <RunServerPage onStatusChange={this.updateStatus} /> )} />
              <Route path="/configure" render={(props) => ( <ConfigurePage onStatusChange={this.updateStatus} /> )} />
              <Route path="/run-monkey" render={(props) => ( <RunMonkeyPage onStatusChange={this.updateStatus} /> )} />
              <Route path="/infection/map" render={(props) => ( <MapPage onStatusChange={this.updateStatus} /> )} />
              <Route path="/infection/logs" render={(props) => ( <FullLogsPage onStatusChange={this.updateStatus} /> )} />
              <Route path="/start-over" render={(props) => ( <StartOverPage onStatusChange={this.updateStatus} /> )} />
              <Route path="/report" render={(props) => ( <ReportPage onStatusChange={this.updateStatus} /> )} />
            </Col>
          </Row>
        </Grid>
      </Router>
    );
  }
}

AppComponent.defaultProps = {};

export default AppComponent;
