import React from 'react';
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons';
import {IslandRoutes} from '../Main';
import VersionComponent from './VersionComponent';

const akamaiLogoImage = require('../../images/akamai-logo.svg');

function Logo() {
  return (
    <>
      <hr/>
      <div className='akamai-link text-center' style={{'marginBottom': '0.5em'}}>
        <span>Powered by</span>
        <a href='https://www.akamai.com/products/akamai-segmentation' rel='noopener noreferrer' target='_blank'>
          <img src={akamaiLogoImage} alt='Akamai'/>
        </a>
      </div>
      <div className='license-link text-center'>
        <a href='https://techdocs.akamai.com/infection-monkey/docs' rel="noopener noreferrer" target="_blank">
          <FontAwesomeIcon icon={faExternalLinkAlt} /> Documentation
        </a>
        <br/>
        <Link to={IslandRoutes.LicensePage}>License</Link>
      </div>
      <VersionComponent/>
    </>
  );
}

export default Logo;
