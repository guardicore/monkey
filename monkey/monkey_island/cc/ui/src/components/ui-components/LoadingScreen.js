import React from 'react';
import monkeyLoader from '../../images/monkey_loading.gif';
import '../../styles/components/LoadingScreen.scss';
import ParticleBackground from './ParticleBackground';

export default function LoadingScreen(props) {
  return (
    <div className={'loading-screen'}>
      <ParticleBackground/>
      <div className={'loading-component'}>
        <div className={'loading-image'}><img src={monkeyLoader}/></div>
        <div className={'loading-text'}>{props.text.toUpperCase()}</div>
      </div>
    </div>);
}
