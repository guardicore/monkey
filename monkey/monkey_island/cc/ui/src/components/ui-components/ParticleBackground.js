import Particles from 'react-particles-js';
import {particleParams} from '../../styles/components/particle-component/ParticleBackgroundParams';
import React from 'react';

export default function ParticleBackground() {
  return (<Particles className={'particle-background'} params={particleParams}/>);
}
