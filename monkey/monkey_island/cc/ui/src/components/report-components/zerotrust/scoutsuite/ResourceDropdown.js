import React, {useState} from 'react';
import * as PropTypes from 'prop-types';
import '../../../../styles/components/scoutsuite/RuleDisplay.scss'
import classNames from 'classnames';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faChevronDown} from '@fortawesome/free-solid-svg-icons/faChevronDown';
import {faChevronUp} from '@fortawesome/free-solid-svg-icons/faChevronUp';
import ScoutSuiteDataParser from './ScoutSuiteDataParser';
import Collapse from '@kunukn/react-collapse';
import {faArrowRight} from '@fortawesome/free-solid-svg-icons';

export default function ResourceDropdown(props) {

  const [isCollapseOpen, setIsCollapseOpen] = useState(false);

  function getResourceDropdown() {
    return (
      <div key={props.resource_path} className={classNames('collapse-item',
        'resource-collapse', {'item--active': isCollapseOpen})}>
        <button className={'btn-collapse'}
                onClick={() => setIsCollapseOpen(!isCollapseOpen)}>
          <span>
            {props.resource_path}
          </span>
          <span>
              <FontAwesomeIcon icon={isCollapseOpen ? faChevronDown : faChevronUp}/>
          </span>
        </button>
        <Collapse
          className='collapse-comp'
          isOpen={isCollapseOpen}
          render={getResourceDropdownContents}/>
      </div>
    );
  }

  function replacePathDotsWithArrows(resourcePath) {
    let path_vars = resourcePath.split('.')
    let display_path = []
    for(let i = 0; i < path_vars.length; i++){
      display_path.push(path_vars[i])
      if( i !== path_vars.length - 1) {
        display_path.push(<FontAwesomeIcon icon={faArrowRight} />)
      }
    }
    return display_path;
  }

  function prettyPrintJson(data) {
    return JSON.stringify(data, null, 4);
  }

  function getResourceDropdownContents() {
    let parser = new ScoutSuiteDataParser(props.scoutsuite_data.data.services);
    return (
      <div className={'resource-display'}>
        <div>
          <p className={'resource-path-title'}>Path:</p>
          <p className={'resource-path-contents'}>{replacePathDotsWithArrows(props.resource_path)}</p>
        </div>
        <div>
          <p className={'resource-value-title'}>Value:</p>
          <pre className={'resource-value-json'}>{prettyPrintJson(parser.getValueAt(props.resource_path))}</pre>
        </div>
      </div>
    );
  }

  return getResourceDropdown();
}

ResourceDropdown.propTypes = {
  resource_path: PropTypes.object,
  scoutsuite_data: PropTypes.object
};
