import Particles from 'react-tsparticles';
import {particleParams} from '../../styles/components/particle-component/ParticleBackgroundParams';
import React from 'react';

export default function ParticleBackground() {
  return (<Particles className={'particle-background'} options={particleParams}/>);
}
