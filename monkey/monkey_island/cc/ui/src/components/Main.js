import React from 'react';
import {BrowserRouter as Router, Redirect, Route, Switch} from 'react-router-dom';
import {Container} from 'react-bootstrap';

import RunServerPage from 'components/pages/RunServerPage';
import ConfigurePage from 'components/pages/ConfigurePage';
import RunMonkeyPage from 'components/pages/RunMonkeyPage/RunMonkeyPage';
import MapPage from 'components/pages/MapPage';
import TelemetryPage from 'components/pages/TelemetryPage';
import StartOverPage from 'components/pages/StartOverPage';
import ReportPage from 'components/pages/ReportPage';
import LicensePage from 'components/pages/LicensePage';
import AuthComponent from 'components/AuthComponent';
import LoginPageComponent from 'components/pages/LoginPage';
import RegisterPageComponent from 'components/pages/RegisterPage';
import Notifier from 'react-desktop-notification';
import NotFoundPage from 'components/pages/NotFoundPage';


import 'normalize.css/normalize.css';
import 'react-data-components/css/table-twbs.css';
import 'styles/App.css';
import 'react-toggle/style.css';
import 'react-table/react-table.css';
import notificationIcon from '../images/notification-logo-512x512.png';
import {StandardLayoutComponent} from './layouts/StandardLayoutComponent';
import LoadingScreen from './ui-components/LoadingScreen';

const reportZeroTrustRoute = '/report/zeroTrust';

class AppComponent extends AuthComponent {
  updateStatus = () => {
    if (this.state.isLoggedIn === false) {
      return
    }
    this.auth.loggedIn()
      .then(res => {
        if (this.state.isLoggedIn !== res) {
          this.setState({
            isLoggedIn: res
          });
        }

        if (!res) {
          this.auth.needsRegistration()
            .then(result => {
              this.setState({
                needsRegistration: result
              });
            })
        }

        if (res) {
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
                this.showInfectionDoneNotification();
              }
            });
        }
      });
  };

  renderRoute = (route_path, page_component, is_exact_path = false) => {
    let render_func = () => {
      switch (this.state.isLoggedIn) {
        case true:
          return page_component;
        case false:
          switch (this.state.needsRegistration) {
            case true:
              return <Redirect to={{pathname: '/register'}}/>
            case false:
              return <Redirect to={{pathname: '/login'}}/>;
            default:
              return <LoadingScreen text={'Loading page...'}/>;
          }
        default:
          return <LoadingScreen text={'Loading page...'}/>;
      }
    };

    if (is_exact_path) {
      return <Route exact path={route_path} render={render_func}/>;
    } else {
      return <Route path={route_path} render={render_func}/>;
    }
  };

  redirectTo = (userPath, targetPath) => {
    let pathQuery = new RegExp(userPath + '[/]?$', 'g');
    if (window.location.pathname.match(pathQuery)) {
      return <Redirect to={{pathname: targetPath}}/>
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      completedSteps: {
        run_server: true,
        run_monkey: false,
        infection_done: false,
        report_done: false,
        isLoggedIn: undefined,
        needsRegistration: undefined
      },
      noAuthLoginAttempted: undefined
    };
  }

  componentDidMount() {
    this.updateStatus();
    this.interval = setInterval(this.updateStatus, 10000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    return (
      <Router>
        <Container fluid>
          <Switch>
            <Route path='/login' render={() => (<LoginPageComponent onStatusChange={this.updateStatus}/>)}/>
            <Route path='/register' render={() => (<RegisterPageComponent onStatusChange={this.updateStatus}/>)}/>
            {this.renderRoute('/',
              <StandardLayoutComponent component={RunServerPage}
                                       completedSteps={this.state.completedSteps}
                                       onStatusChange={this.updateStatus}
              />,
              true)}
            {this.renderRoute('/configure',
              <StandardLayoutComponent component={ConfigurePage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/run-monkey',
              <StandardLayoutComponent component={RunMonkeyPage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/infection/map',
              <StandardLayoutComponent component={MapPage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/infection/telemetry',
              <StandardLayoutComponent component={TelemetryPage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/start-over',
              <StandardLayoutComponent component={StartOverPage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.redirectTo('/report', '/report/security')}
            {this.renderRoute('/report/security',
              <StandardLayoutComponent component={ReportPage}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/report/attack',
              <StandardLayoutComponent component={ReportPage}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/report/zeroTrust',
              <StandardLayoutComponent component={ReportPage}
                                       completedSteps={this.state.completedSteps}/>)}
            {this.renderRoute('/license',
              <StandardLayoutComponent component={LicensePage}
                                       onStatusChange={this.updateStatus}
                                       completedSteps={this.state.completedSteps}/>)}
            <Route component={NotFoundPage}/>
          </Switch>
        </Container>
      </Router>
    );
  }

  showInfectionDoneNotification() {
    if (this.shouldShowNotification()) {
      const hostname = window.location.hostname;
      const port = window.location.port;
      const protocol = window.location.protocol;
      const url = `${protocol}//${hostname}:${port}${reportZeroTrustRoute}`;

      Notifier.start(
        'Monkey Island',
        'Infection is done! Click here to go to the report page.',
        url,
        notificationIcon);
    }
  }

  shouldShowNotification() {
    // No need to show the notification to redirect to the report if we're already in the report page
    return (this.state.completedSteps.infection_done && !window.location.pathname.startsWith('/report'));
  }
}

AppComponent.defaultProps = {};

export default AppComponent;
