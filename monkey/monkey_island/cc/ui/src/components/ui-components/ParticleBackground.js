import Particles from 'react-tsparticles';
import {particleParams} from '../../styles/components/particle-component/ParticleBackgroundParams';
import React, {useCallback} from 'react';
import {loadFull} from 'tsparticles';

export default function ParticleBackground() {
  const particlesInit = useCallback(async engine => {
        await loadFull(engine);
    }, []);

  const particlesLoaded = useCallback(async container => {
        await container;
    }, []);

  return (
    <Particles init={particlesInit} className={'particle-background'} loaded={particlesLoaded} options={particleParams}/>
  );
}
