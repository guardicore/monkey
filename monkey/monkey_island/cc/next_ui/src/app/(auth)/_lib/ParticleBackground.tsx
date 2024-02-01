import { useEffect, useMemo, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import {
    type Container,
    type ISourceOptions,
    MoveDirection,
    OutMode
} from '@tsparticles/engine';
import { loadLinksPreset } from '@tsparticles/preset-links'; // if you are going to use `loadLinksPreset`, install the "@tsparticles/presets" package too.

const ParticleBackground = () => {
    const [init, setInit] = useState(false);

    // this should be run only once per application lifetime
    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadLinksPreset(engine);
        }).then(() => {
            setInit(true);
        });
    }, []);

    const particlesLoaded = async (container?: Container): Promise<void> => {
        console.log(container);
    };

    const options: ISourceOptions = useMemo(
        () => ({
            preset: 'links',
            background: {
                color: '#ffffff'
            },
            particles: {
                color: { value: '#eeb818' },
                links: {
                    color: '#eeb818',
                    distance: 150,
                    enable: true,
                    opacity: 0.7,
                    width: 2
                },
                move: {
                    bounce: false,
                    direction: 'none',
                    enable: true,
                    outMode: 'out',
                    random: false,
                    speed: 2,
                    straight: false
                }
            },
            detectRetina: true
        }),
        []
    );

    if (init) {
        return (
            <Particles
                id="tsparticles"
                particlesLoaded={particlesLoaded}
                options={options}
                style={{ zIndex: -100 }}
            />
        );
    }

    return <></>;
};

export default ParticleBackground;
