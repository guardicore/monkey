import React, {ReactFragment} from 'react';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faUndo} from '@fortawesome/free-solid-svg-icons/faUndo';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons';
import VersionComponent from './side-menu/VersionComponent';
import '../styles/components/SideNav.scss';
import {CompletedSteps} from "./side-menu/CompletedSteps";
import {isReportRoute, Routes} from "./Main";


const guardicoreLogoImage = require('../images/guardicore-logo.png');
const logoImage = require('../images/monkey-icon.svg');
const infectionMonkeyImage = require('../images/infection-monkey.svg');


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

      <div className={getNavSectionClass()}>
        <ul className='navigation'>
          <>
            <li>
              {header}
            </li>
            <hr />
          </>

          <li>
            <NavLink to={Routes.RunMonkeyPage}>
              <span className='number'>1.</span>
              Run Monkey
              {completedSteps.runMonkey ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to={Routes.MapPage}>
              <span className='number'>2.</span>
              Infection Map
              {completedSteps.infectionDone ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to={defaultReport}
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
            <NavLink to={Routes.StartOverPage}>
              <span className='number'><FontAwesomeIcon icon={faUndo} style={{'marginLeft': '-1px'}}/></span>
              Start Over
            </NavLink>
          </li>
        </ul>

        <hr />
        <ul>
          <li><NavLink to={Routes.ConfigurePage}>
            Configuration
          </NavLink></li>
          <li><NavLink to='/infection/telemetry'>
            Logs
          </NavLink></li>
        </ul>
      </div>

      <hr />
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
        <NavLink to={Routes.LicensePage}>License</NavLink>
      </div>
      <VersionComponent/>
    </>);

  function getNavSectionClass() {
    if(disabled){
      return 'placeholder'
    } else {
      return ''
    }
  }
}

export default SideNavComponent;
