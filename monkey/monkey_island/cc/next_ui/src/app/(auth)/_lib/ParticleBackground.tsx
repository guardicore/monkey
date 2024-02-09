import { useEffect, useMemo, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadLinksPreset } from '@tsparticles/preset-links';
import { useTheme } from '@mui/material/styles';
import { ISourceOptions } from '@tsparticles/engine';

const ParticleBackground = () => {
    const [init, setInit] = useState(false);
    const theme = useTheme();

    // this should be run only once per application lifetime
    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadLinksPreset(engine);
        }).then(() => {
            setInit(true);
        });
    }, []);

    //@ts-ignore
    const options: ISourceOptions = useMemo(
        () => ({
            preset: 'links',
            // All the options for links preset are defined below
            background: {
                color: `${theme.palette.background.default}`
            },
            particles: {
                color: `${theme.palette.secondary.main}`,
                number: {
                    value: 100
                },
                links: {
                    color: `${theme.palette.secondary.main}`,
                    distance: 150,
                    enable: true
                },
                move: {
                    enable: true
                },
                size: {
                    value: 1
                },
                shape: {
                    type: 'circle'
                }
            }
        }),
        [theme]
    );

    if (init) {
        // @ts-ignore
        return (
            <Particles
                id="tsparticles"
                options={options}
                style={{ zIndex: -100 }}
            />
        );
    }

    return <></>;
};

export default ParticleBackground;
