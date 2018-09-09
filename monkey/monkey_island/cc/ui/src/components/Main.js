import React from 'react';
import {BrowserRouter as Router, NavLink, Redirect, Route} from 'react-router-dom';
import {Col, Grid, Row} from 'react-bootstrap';
import {Icon} from 'react-fa';

import RunServerPage from 'components/pages/RunServerPage';
import ConfigurePage from 'components/pages/ConfigurePage';
import RunMonkeyPage from 'components/pages/RunMonkeyPage';
import MapPage from 'components/pages/MapPage';
import TelemetryPage from 'components/pages/TelemetryPage';
import StartOverPage from 'components/pages/StartOverPage';
import ReportPage from 'components/pages/ReportPage';
import LicensePage from 'components/pages/LicensePage';
import AuthComponent from 'components/AuthComponent';
import LoginPageComponent from 'components/pages/LoginPage';

import 'normalize.css/normalize.css';
import 'react-data-components/css/table-twbs.css';
import 'styles/App.css';
import 'react-toggle/style.css';
import 'react-table/react-table.css';

let logoImage = require('../images/monkey-icon.svg');
let infectionMonkeyImage = require('../images/infection-monkey.svg');
let guardicoreLogoImage = require('../images/guardicore-logo.png');

class AppComponent extends AuthComponent {
  updateStatus = () => {
    if (this.auth.loggedIn()){
      this.authFetch('/api')
        .then(res => res.json())
        .then(res => {
          // This check is used to prevent unnecessary re-rendering
          let isChanged = false;
          for (let step in this.state.completedSteps) {
            if (this.state.completedSteps[step] !== res['completed_steps'][step]) {
              isChanged = true;
              break;
            }
          }
          if (isChanged) {
            this.setState({completedSteps: res['completed_steps']});
          }
        });
    }
  };

  renderRoute = (route_path, page_component, is_exact_path = false) => {
    let render_func = (props) => {
      if (this.auth.loggedIn()) {
        return page_component;
      } else {
        return <Redirect to={{pathname: '/login'}}/>;
      }
    };

    if (is_exact_path) {
      return <Route exact path={route_path} render={render_func}/>;
    } else {
      return <Route path={route_path} render={render_func}/>;
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      completedSteps: {
        run_server: true,
        run_monkey: false,
        infection_done: false,
        report_done: false
      }
    };
  }

  componentDidMount() {
    this.updateStatus();
    this.interval = setInterval(this.updateStatus, 2000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    return (
      <Router>
        <Grid fluid={true}>
          <Row>
            <Col sm={3} md={2} className="sidebar">
              <div className="header">
                <img src={logoImage} style={{width: '5vw', margin: '15px'}}/>
                <img src={infectionMonkeyImage} style={{width: '15vw'}} alt="Infection Monkey"/>
              </div>

              <ul className="navigation">
                <li>
                  <NavLink to="/" exact={true}>
                    <span className="number">1.</span>
                    Run Monkey Island Server
                    {this.state.completedSteps.run_server ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/run-monkey">
                    <span className="number">2.</span>
                    Run Monkey
                    {this.state.completedSteps.run_monkey ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/infection/map">
                    <span className="number">3.</span>
                    Infection Map
                    {this.state.completedSteps.infection_done ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/report">
                    <span className="number">4.</span>
                    Security Report
                    {this.state.completedSteps.report_done ?
                      <Icon name="check" className="pull-right checkmark text-success"/>
                      : ''}
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/start-over">
                    <span className="number"><i className="fa fa-undo" style={{'marginLeft': '-1px'}}/></span>
                    Start Over
                  </NavLink>
                </li>
              </ul>

              <hr/>
              <ul>
                <li><NavLink to="/configure">Configuration</NavLink></li>
                <li><NavLink to="/infection/telemetry">Log</NavLink></li>
              </ul>

              <hr/>
              <div className="guardicore-link text-center" style={{'marginBottom': '0.5em'}}>
                <span>Powered by</span>
                <a href="http://www.guardicore.com" target="_blank">
                  <img src={guardicoreLogoImage} alt="GuardiCore"/>
                </a>
              </div>
              <div className="license-link text-center">
                <NavLink to="/license">License</NavLink>
              </div>
            </Col>
            <Col sm={9} md={10} smOffset={3} mdOffset={2} className="main">
              <Route path='/login' render={(props) => (<LoginPageComponent onStatusChange={this.updateStatus}/>)}/>
              {this.renderRoute('/', <RunServerPage onStatusChange={this.updateStatus}/>, true)}
              {this.renderRoute('/configure', <ConfigurePage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/run-monkey', <RunMonkeyPage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/infection/map', <MapPage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/infection/telemetry', <TelemetryPage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/start-over', <StartOverPage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/report', <ReportPage onStatusChange={this.updateStatus}/>)}
              {this.renderRoute('/license', <LicensePage onStatusChange={this.updateStatus}/>)}
            </Col>
          </Row>
        </Grid>
      </Router>
    );
  }
}

AppComponent.defaultProps = {};

export default AppComponent;
