import React from 'react';

import '../../styles/NotFoundPage.scss';

let monkeyDetective = require('../../images/detective-monkey.svg');

class ConfigurePageComponent extends React.Component{
  constructor(props) {
    super(props);
    }

  render(){
    return(
      <div className={'not-found'}>
        <img className={'monkey-detective'} src={monkeyDetective}/>
        <div className={'text-block'}>
          <h1 className={'not-found-title'}>404</h1>
          <h2 className={'not-found-subtitle'}>Page not found</h2>
        </div>
      </div>
    )
  }
}

export default ConfigurePageComponent;
