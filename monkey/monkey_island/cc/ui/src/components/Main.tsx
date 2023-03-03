import React from 'react';
import {BrowserRouter as Router, Redirect, Route, Switch} from 'react-router-dom';
import {Container} from 'react-bootstrap';

import ConfigurePage from './pages/ConfigurePage.js';
import RunMonkeyPage from './pages/RunMonkeyPage/RunMonkeyPage';
import MapPageWrapper from './map/MapPageWrapper';
import EventPage from './pages/EventPage';
import ReportPage from './pages/ReportPage';
import LicensePage from './pages/LicensePage';
import AuthComponent from './AuthComponent';
import LoginPageComponent from './pages/LoginPage';
import RegisterPageComponent from './pages/RegisterPage';
import LandingPage from "./pages/LandingPage";
import Notifier from 'react-desktop-notification';
import NotFoundPage from './pages/NotFoundPage';
import GettingStartedPage from './pages/GettingStartedPage';


import 'normalize.css/normalize.css';
import 'styles/App.css';
import 'react-table/react-table.css';
import LoadingScreen from './ui-components/LoadingScreen';
import SidebarLayoutComponent from "./layouts/SidebarLayoutComponent";
import {CompletedSteps} from "./side-menu/CompletedSteps";
import Timeout = NodeJS.Timeout;
import IslandHttpClient, { APIEndpoint } from "./IslandHttpClient";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFileCode, faLightbulb} from "@fortawesome/free-solid-svg-icons";
import { doesAnyAgentExist, didAllAgentsShutdown } from './utils/ServerUtils';
import AuthService from '../services/AuthService';

let notificationIcon = require('../images/notification-logo-512x512.png');

export const Routes = {
  LandingPage: '/landing-page',
  GettingStartedPage: '/',
  Report: '/report',
  SecurityReport: '/report/security',
  RansomwareReport: '/report/ransomware',
  LoginPage: '/login',
  RegisterPage: '/register',
  Logout: '/logout',
  ConfigurePage: '/configure',
  RunMonkeyPage: '/run-monkey',
  MapPage: '/infection/map',
  EventPage: '/infection/events',
  LicensePage: '/license'
}

export function isReportRoute(route){
  return route.startsWith(Routes.Report);
}

class AppComponent extends AuthComponent {
  private interval: Timeout;

  constructor(props) {
    super(props);
    this.state = {
      completedSteps: new CompletedSteps(false),
      islandMode: undefined,
    };
    this.interval = undefined;
    this.setMode();
  }

  updateStatus = () => {
    if (this.state.isLoggedIn === false) {
      return
    }

    let res = this.auth.loggedIn();

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
      this.setMode()
        .then(() => {
          if (this.state.islandMode === "unset") {
            return
          }

          // update status: report generation
          this.authFetch('/api/report-generation-status')
            .then(res => res.json())
            .then(res => {
              this.setState({
                completedSteps: new CompletedSteps(
                                      this.state.completedSteps.runMonkey,
                                      this.state.completedSteps.infectionDone,
                                      res.report_done
                                    )
              });
            })

          // update status: if any agent ran
          doesAnyAgentExist().then(anyAgentExists => {
            this.setState({
              completedSteps: new CompletedSteps(
                                    anyAgentExists,
                                    this.state.completedSteps.infectionDone,
                                    this.state.completedSteps.reportDone
                                  )
            });
          });

          // update status: if infection (running and shutting down of all agents) finished
          didAllAgentsShutdown().then(allAgentsShutdown => {
            let infectionDone = this.state.completedSteps.runMonkey && allAgentsShutdown;
            if(this.state.completedSteps.infectionDone === false
              && infectionDone){
              this.showInfectionDoneNotification();
            }
            this.setState({
              completedSteps: new CompletedSteps(
                                    this.state.completedSteps.runMonkey,
                                    infectionDone,
                                    this.state.completedSteps.reportDone
                                  )
            });
          });
        }
      )
    }
  };

  setMode = () => {
    return IslandHttpClient.get(APIEndpoint.mode)
      .then(res => {
        this.setState({islandMode: res.body});
      });
  }

  renderRoute = (route_path, page_component, is_exact_path = false) => {
    let render_func = () => {
      switch (this.state.isLoggedIn) {
        case true:
          if (this.needsRedirectionToLandingPage(route_path)) {
            return <Redirect to={{pathname: Routes.LandingPage}}/>
          } else if (this.needsRedirectionToGettingStarted(route_path)) {
            return <Redirect to={{pathname: Routes.GettingStartedPage}}/>
          }
          return page_component;
        case false:
          switch (this.state.needsRegistration) {
            case true:
              return <Redirect to={{pathname: Routes.RegisterPage}}/>
            case false:
              return <Redirect to={{pathname: Routes.LoginPage}}/>;
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

  needsRedirectionToLandingPage = (route_path) => {
    return (this.state.islandMode === "unset" && route_path !== Routes.LandingPage)
  }

  needsRedirectionToGettingStarted = (route_path) => {
    return route_path === Routes.LandingPage &&
      this.state.islandMode !== "unset" && this.state.islandMode !== undefined
  }

  redirectTo = (userPath, targetPath) => {
    let pathQuery = new RegExp(userPath + '[/]?$', 'g');
    if (window.location.pathname.match(pathQuery)) {
      return <Redirect to={{pathname: targetPath}}/>
    }
  };

  componentDidMount() {
    this.updateStatus();
    this.interval = setInterval(this.updateStatus, 10000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  getDefaultReport() {
    if(this.state.islandMode === 'ransomware'){
      return Routes.RansomwareReport;
    } else {
      return Routes.SecurityReport;
    }
  }

  getIslandModeTitle(){
    if(this.state.islandMode === 'ransomware'){
      return this.formIslandModeTitle("Ransomware", faFileCode);
    } else {
      return this.formIslandModeTitle("Custom", faLightbulb);
    }
  }

  formIslandModeTitle(title, icon){
    return (<>
      <h5 className={'text-muted'}>
        <FontAwesomeIcon icon={icon} /> {title}
      </h5>
    </>)
  }

  render() {

    let defaultSideNavProps = {completedSteps: this.state.completedSteps,
                               onStatusChange: this.updateStatus,
                               islandMode: this.state.islandMode,
                               defaultReport: this.getDefaultReport(),
                               sideNavHeader: this.getIslandModeTitle()}

    return (
      <Router>
        <Container fluid>
          <Switch>
            <Route path={Routes.LoginPage} render={() => (<LoginPageComponent onStatusChange={this.updateStatus}/>)}/>
            <Route path={Routes.Logout} render={async () => ( await new AuthService().logout()
              .then(() => (<Redirect to={'/'} />)))}/>
            <Route path={Routes.RegisterPage} render={() => (<RegisterPageComponent onStatusChange={this.updateStatus}/>)}/>
            {this.renderRoute(Routes.LandingPage,
              <SidebarLayoutComponent component={LandingPage}
                                      sideNavShow={false}
                                      sideNavDisabled={true}
                                      completedSteps={new CompletedSteps()}
                                      onStatusChange={this.updateStatus}/>)}
            {this.renderRoute(Routes.GettingStartedPage,
              <SidebarLayoutComponent component={GettingStartedPage} {...defaultSideNavProps}/>,
              true)}
            {this.renderRoute(Routes.ConfigurePage,
              <SidebarLayoutComponent component={ConfigurePage} {...defaultSideNavProps}/>)}
            {this.renderRoute(Routes.RunMonkeyPage,
              <SidebarLayoutComponent component={RunMonkeyPage} {...defaultSideNavProps}/>)}
            {this.renderRoute(Routes.MapPage,
              <SidebarLayoutComponent component={MapPageWrapper} {...defaultSideNavProps}/>)}
            {this.renderRoute(Routes.EventPage,
              <SidebarLayoutComponent component={EventPage} {...defaultSideNavProps}/>)}
            {this.redirectToReport()}
            {this.renderRoute(Routes.SecurityReport,
              <SidebarLayoutComponent component={ReportPage}
                                      islandMode={this.state.islandMode}
                                      {...defaultSideNavProps}/>)}
            {this.renderRoute(Routes.RansomwareReport,
              <SidebarLayoutComponent component={ReportPage}
                                      islandMode={this.state.islandMode}
                                      {...defaultSideNavProps}/>)}
            {this.renderRoute(Routes.LicensePage,
              <SidebarLayoutComponent component={LicensePage}
                                      islandMode={this.state.islandMode}
                                      {...defaultSideNavProps}/>)}
            <Route component={NotFoundPage}/>
          </Switch>
        </Container>
      </Router>
    );
  }

  redirectToReport() {
    if (this.state.islandMode === 'ransomware') {
      return this.redirectTo(Routes.Report, Routes.RansomwareReport)
    } else {
      return this.redirectTo(Routes.Report, Routes.SecurityReport)
    }
  }

  showInfectionDoneNotification() {
    if (!window.location.pathname.startsWith(Routes.Report)) {
      const hostname = window.location.hostname;
      const port = window.location.port;
      const protocol = window.location.protocol;
      const url = `${protocol}//${hostname}:${port}${Routes.SecurityReport}`;

      Notifier.start(
        'Monkey Island',
        'Infection is done! Click here to go to the report page.',
        url,
        notificationIcon);
    }
  }
}

export default AppComponent;
