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
            preset: 'links'
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
