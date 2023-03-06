import React, {ReactFragment, useState} from 'react';
import {Button} from 'react-bootstrap';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faUndo} from '@fortawesome/free-solid-svg-icons/faUndo';
import '../styles/components/SideNav.scss';
import {CompletedSteps} from './side-menu/CompletedSteps';
import {isReportRoute, routes} from './Main';
import Logo from './logo/LogoComponent';
import IslandResetModal from './ui-components/IslandResetModal';


const logoImage = require('../images/monkey-icon.svg');
const infectionMonkeyImage = require('../images/infection-monkey.svg');

type Props = {
  disabled?: boolean,
  completedSteps: CompletedSteps,
  defaultReport: string,
  header?: ReactFragment,
  onStatusChange: () => void
};


const SideNavComponent = ({
                            disabled,
                            completedSteps,
                            defaultReport,
                            header = null,
                            onStatusChange,
                          }: Props) => {

  const [showResetModal, setShowResetModal] = useState(false);

  return (
    <>
      <NavLink to={routes.GettingStartedPage} end>
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
          <NavLink to={routes.RunMonkeyPage} className={getNavLinkClass()}>
            <span className='number'>1.</span>
            Run Monkey
            {completedSteps.runMonkey ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <NavLink to={routes.MapPage} className={getNavLinkClass()}>
            <span className='number'>2.</span>
            Infection Map
            {completedSteps.infectionDone ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <NavLink to={defaultReport}
                   className={(isReportRoute(location.pathname) ? 'active' : 'inactive') + ' ' + getNavLinkClass()}
                   >
            <span className='number'>3.</span>
            Security Reports
            {completedSteps.reportDone ?
              <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
              : ''}
          </NavLink>
        </li>
        <li>
          <Button variant={null} className={'island-reset-button'}
                  onClick={() => setShowResetModal(true)} href='#'>
            <span className='number'><FontAwesomeIcon icon={faUndo} style={{'marginLeft': '-1px'}}/></span>
            Reset
          </Button>
          <IslandResetModal show={showResetModal}
                            allMonkeysAreDead={areMonkeysDead()}
                            onReset={onStatusChange}
                            onClose={() => {
                              setShowResetModal(false);
                            }}/>
        </li>
      </ul>

      <hr/>
      <ul>
        <li><NavLink to={routes.ConfigurePage}
                     className={getNavLinkClass()}>
          Configuration
        </NavLink></li>
        <li><NavLink to='/infection/events'
                     className={getNavLinkClass()}>
          Events
        </NavLink></li>
      </ul>

      <Logo/>
    </>);

  function areMonkeysDead() {
    return (!completedSteps['runMonkey']) || (completedSteps['infectionDone'])
  }

  function getNavLinkClass() {
    if (disabled) {
      return `nav-link disabled`
    } else {
      return ''
    }
  }
}

export default SideNavComponent;
