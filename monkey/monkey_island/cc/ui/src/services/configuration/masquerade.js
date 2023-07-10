export const DEFAULT_MASQUES_VALUES = {
    texts: [],
    base64: ''
};
export const DEFAULT_MASQUES = {
    linux: { ...DEFAULT_MASQUES_VALUES },
    windows: { ...DEFAULT_MASQUES_VALUES }
};
export const MASQUERADE = {
    title: 'Masquerade',
    type: 'object',
    description:
        'Infection Monkey can mimic a malware signature by injecting data into ' +
        'Agent binaries.\nThis feature can be particularly helpful when testing custom malware ' +
        'detection rules.',
    properties: {
        linux: {
            title: 'Linux Masque',
            properties: {
                masque_texts: {
                    title: 'Texts',
                    type: 'array',
                    uniqueItems: true,
                    items: { type: 'string' },
                    default: DEFAULT_MASQUES.linux.texts,
                    description:
                        'List of masque strings that will be included in the Linux Agent binary.'
                },
                masque_base64: {
                    title: 'Base64',
                    type: 'string',
                    format: 'valid-base64',
                    default: DEFAULT_MASQUES.linux.base64,
                    description:
                        'A masque (bytes) encoded in Base64 that will be included in the Linux Agent binary.'
                }
            }
        },
        windows: {
            title: 'Windows Masque',
            properties: {
                masque_texts: {
                    title: 'Texts',
                    type: 'array',
                    uniqueItems: true,
                    items: { type: 'string' },
                    default: DEFAULT_MASQUES.windows.texts,
                    description:
                        'List of masque strings that will be included in the Windows Agent binary.'
                },
                masque_base64: {
                    title: 'Base64',
                    type: 'string',
                    format: 'valid-base64',
                    default: DEFAULT_MASQUES.windows.base64,
                    description:
                        'A masque (bytes) encoded in Base64 that will be included in the Windows Agent binary.'
                }
            }
        }
    }
};
