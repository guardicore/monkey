import React, {ReactFragment} from 'react';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faUndo} from '@fortawesome/free-solid-svg-icons/faUndo';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons';
import '../styles/components/SideNav.scss';
import {CompletedSteps} from "./side-menu/CompletedSteps";
import {isReportRoute, Routes} from "./Main";


const logoImage = require('../images/monkey-icon.svg');
const infectionMonkeyImage = require('../images/infection-monkey.svg');

import Logo from "./logo/LogoComponent";

type Props = {
  disabled?: boolean,
  completedSteps: CompletedSteps,
  defaultReport: string,
  header?: ReactFragment
}


const SideNavComponent = ({disabled,
                           completedSteps,
                           defaultReport,
                           header=null}: Props) => {

  return (
    <>
      <NavLink to={Routes.GettingStartedPage} exact={true}>
        <div className='header'>
          <img alt='logo' src={logoImage} style={{width: '5vw', margin: '15px'}}/>
          <img src={infectionMonkeyImage} style={{width: '15vw'}} alt='Infection Monkey'/>
        </div>
      </NavLink>

      <ul className='navigation'>
        {(header !== null) &&
        <>
          <li>
            {header}
          </li>
          <hr/>
        </>}

        <li>
          <NavLink to={Routes.RunMonkeyPage} className={getNavLinkClass()}>
            <span className='number'>1.</span>
            Run Monkey
            {completedSteps.runMonkey ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <NavLink to={Routes.MapPage} className={getNavLinkClass()}>
            <span className='number'>2.</span>
            Infection Map
            {completedSteps.infectionDone ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <NavLink to={defaultReport}
                   className={getNavLinkClass()}
                   isActive={(_match, location) => {
                     return (isReportRoute(location.pathname))
                   }}>
            <span className='number'>3.</span>
            Security Reports
            {completedSteps.reportDone ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <NavLink to={Routes.StartOverPage} className={getNavLinkClass()}>
            <span className='number'><FontAwesomeIcon icon={faUndo} style={{'marginLeft': '-1px'}}/></span>
            Start Over
          </NavLink>
        </li>
      </ul>

      <hr/>
      <ul>
        <li><NavLink to={Routes.ConfigurePage}
                     className={getNavLinkClass()}>
          Configuration
        </NavLink></li>
        <li><NavLink to='/infection/telemetry'
        className={getNavLinkClass()}>
          Logs
        </NavLink></li>
      </ul>

      <Logo/>
    </>);

  function getNavLinkClass() {
    if(disabled){
      return `nav-link disabled`
    } else {
      return ''
    }
  }
}

export default SideNavComponent;
