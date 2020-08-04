import React from 'react';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faUndo} from '@fortawesome/free-solid-svg-icons/faUndo';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons';
import guardicoreLogoImage from '../images/guardicore-logo.png';
import logoImage from '../images/monkey-icon.svg';
import infectionMonkeyImage from '../images/infection-monkey.svg';
import VersionComponent from './side-menu/VersionComponent';
import '../styles/components/SideNav.scss';


class SideNavComponent extends React.Component {

  render() {
    return (
      <>
        <NavLink to={'/'} exact={true}>
          <div className='header'>
            <img alt='logo' src={logoImage} style={{width: '5vw', margin: '15px'}}/>
            <img src={infectionMonkeyImage} style={{width: '15vw'}} alt='Infection Monkey'/>
          </div>
        </NavLink>

        <ul className='navigation'>
          <li>
            <NavLink to='/run-monkey'>
              <span className='number'>1.</span>
              Run Monkey
              {this.props.completedSteps.run_monkey ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/infection/map'>
              <span className='number'>2.</span>
              Infection Map
              {this.props.completedSteps.infection_done ?
                <FontAwesomeIcon icon={faCheck} className='pull-right checkmark'/>
                : ''}
            </NavLink>
          </li>
          <li>
            <NavLink to='/report/security'
                     isActive={(_match, location) => {
                       return (location.pathname === '/report/attack'
                         || location.pathname === '/report/zeroTrust'
                         || location.pathname === '/report/security')
                     }}>
              <span className='number'>3.</span>
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
          <li><NavLink to='/infection/telemetry'>Logs</NavLink></li>
        </ul>

        <hr/>
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
          <NavLink to='/license'>License</NavLink>
        </div>
        <VersionComponent/>
      </>)
  }
}

export default SideNavComponent;
