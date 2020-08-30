import logoImage from '../images/monkey-icon.svg';
import infectionMonkeyImage from '../images/infection-monkey.svg';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faUndo} from '@fortawesome/free-solid-svg-icons/faUndo';
import guardicoreLogoImage from '../images/guardicore-logo.png';
import VersionComponent from './side-menu/VersionComponent';
import React from 'react';


class SideNavComponent extends React.Component {

  render() {
    return (
      <>
        <div className='header'>
          <img alt='logo' src={logoImage} style={{width: '5vw', margin: '15px'}}/>
          <img src={infectionMonkeyImage} style={{width: '15vw'}} alt='Infection Monkey'/>
        </div>

        <ul className='navigation'>
          <li>
            <NavLink to='/' exact={true}>
              <span className='number'>1.</span>
              Run Monkey Island Server
              {this.props.completedSteps.run_server ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/run-monkey'>
              <span className='number'>2.</span>
              Run Monkey
              {this.props.completedSteps.run_monkey ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/infection/map'>
              <span className='number'>3.</span>
              Infection Map
              {this.props.completedSteps.infection_done ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/report/security'
                     isActive={(match, location) => {
                       return (location.pathname === '/report/attack'
                         || location.pathname === '/report/zeroTrust'
                         || location.pathname === '/report/security')
                     }}>
              <span className='number'>4.</span>
              Security Reports
              {this.props.completedSteps.report_done ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/start-over'>
              <span className='number'><FontAwesomeIcon icon={faUndo} style={{'marginLeft': '-1px'}}/></span>
              Start Over
            </NavLink>
          </li>
        </ul>

        <hr/>
        <ul>
          <li><NavLink to='/configure'>Configuration</NavLink></li>
          <li><NavLink to='/infection/telemetry'>Log</NavLink></li>
        </ul>

        <hr/>
        <div className='guardicore-link text-center' style={{'marginBottom': '0.5em'}}>
          <span>Powered by</span>
          <a href='http://www.guardicore.com' rel='noopener noreferrer' target='_blank'>
            <img src={guardicoreLogoImage} alt='GuardiCore'/>
          </a>
        </div>
        <div className='license-link text-center'>
          <NavLink to='/license'>License</NavLink>
        </div>
        <VersionComponent/>
      </>)
  }
}

export default SideNavComponent;
