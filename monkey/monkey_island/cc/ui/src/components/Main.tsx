import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
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
import Notifier from 'react-desktop-notification';
import NotFoundPage from './pages/NotFoundPage';
import GettingStartedPage from './pages/GettingStartedPage';
import 'normalize.css/normalize.css';
import 'styles/App.css';
import LoadingScreen from './ui-components/LoadingScreen';
import SidebarLayoutComponent from "./layouts/SidebarLayoutComponent";
import {CompletedSteps} from "./side-menu/CompletedSteps";
import Timeout = NodeJS.Timeout;
import IslandHttpClient, { APIEndpoint } from "./IslandHttpClient";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFileCode, faLightbulb} from "@fortawesome/free-solid-svg-icons";
import { doesAnyAgentExist, didAllAgentsShutdown } from './utils/ServerUtils';
import LogoutPage from './pages/LogoutPage';

let notificationIcon = require('../images/notification-logo-512x512.png');

export const IslandRoutes = {
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
  LicensePage: '/license',
  PluginsPage: '/marketplace',
}

export function isReportRoute(route){
  return route.startsWith(IslandRoutes.Report);
}

class AppComponent extends AuthComponent {
  private interval: Timeout;

  constructor(props) {
    super(props);
    this.state = {
      completedSteps: new CompletedSteps(false),
    };
    this.interval = undefined;
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
      // update status: report generation
      this.authFetch('/api/report-generation-status', {}, false)
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
      doesAnyAgentExist(false).then(anyAgentExists => {
        this.setState({
          completedSteps: new CompletedSteps(
                                anyAgentExists,
                                this.state.completedSteps.infectionDone,
                                this.state.completedSteps.reportDone
                              )
        });
      });

      // update status: if infection (running and shutting down of all agents) finished
      didAllAgentsShutdown(false).then(allAgentsShutdown => {
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
  };

  renderRoute = (route_path, page_component) => {
    let render_func = () => {
      switch (this.state.isLoggedIn) {
        case true:
          return page_component;
        case false:
          switch (this.state.needsRegistration) {
            case true:
              return <Navigate replace to={IslandRoutes.RegisterPage}/>;
            case false:
              return <Navigate replace to={IslandRoutes.LoginPage}/>;
            default:
              return <LoadingScreen text={'Loading page...'}/>;
          }
        default:
          return <LoadingScreen text={'Loading page...'}/>;
      }
    };

    return <Route path={route_path} element={render_func()}/>;
  };

  redirectTo = (userPath, targetPath) => {
    let pathQuery = new RegExp(userPath + '[/]?$', 'g');
    if (window.location.pathname.match(pathQuery)) {
      return <Route element={<Navigate replace to={targetPath}/>}/>
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
    return IslandRoutes.SecurityReport;
  }

  render() {

    let defaultSideNavProps = {completedSteps: this.state.completedSteps,
                               onStatusChange: this.updateStatus,
                               defaultReport: this.getDefaultReport(),
                               onLogout: () => {this.auth.logout()
                                 .then(() => this.updateStatus())}};

    return (
      <Router>
        <Container fluid>
          <Routes>
            <Route path={IslandRoutes.LoginPage} element={<LoginPageComponent onStatusChange={this.updateStatus}/>}/>
            <Route path={IslandRoutes.Logout} element={<LogoutPage onStatusChange={this.updateStatus}/>}/>
            <Route path={IslandRoutes.RegisterPage} element={<RegisterPageComponent onStatusChange={this.updateStatus}/>}/>
            {this.renderRoute(IslandRoutes.GettingStartedPage,
              <SidebarLayoutComponent component={GettingStartedPage} {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.ConfigurePage,
              <SidebarLayoutComponent component={ConfigurePage} {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.RunMonkeyPage,
              <SidebarLayoutComponent component={RunMonkeyPage} {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.MapPage,
              <SidebarLayoutComponent component={MapPageWrapper} {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.EventPage,
              <SidebarLayoutComponent component={EventPage} {...defaultSideNavProps}/>)}
            {this.redirectToReport()}
            {this.renderRoute(IslandRoutes.SecurityReport,
              <SidebarLayoutComponent component={ReportPage}
                                      {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.RansomwareReport,
              <SidebarLayoutComponent component={ReportPage}
                                      {...defaultSideNavProps}/>)}
            {this.renderRoute(IslandRoutes.LicensePage,
              <SidebarLayoutComponent component={LicensePage}
                                      {...defaultSideNavProps}/>)}
            <Route path='*' element={<NotFoundPage/>}/>
          </Routes>
        </Container>
      </Router>
    );
  }

  redirectToReport() {
    return this.redirectTo(IslandRoutes.Report, IslandRoutes.SecurityReport)
  }

  showInfectionDoneNotification() {
    if (!window.location.pathname.startsWith(IslandRoutes.Report)) {
      const hostname = window.location.hostname;
      const port = window.location.port;
      const protocol = window.location.protocol;
      const url = `${protocol}//${hostname}:${port}${IslandRoutes.SecurityReport}`;

      Notifier.start(
        'Monkey Island',
        'Infection is done! Click here to go to the report page.',
        url,
        notificationIcon);
    }
  }
}

export default AppComponent;
