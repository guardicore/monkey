export const DEFAULT_MASQUES = {
  linux: {
    texts: [],
    base64: []
  },
  windows: {
    texts: [],
    base64: []
  }
}
export const MASQUERADE = {
  title: 'Masquerade',
  type: 'object',
  description: 'Infection Monkey can mimic a malware signature by injecting custom data into ' +
    'Agent binaries.\nThis feature can be particularly helpful when testing custom detection ' +
    'rules.',
  properties: {
    linux: {
      title: 'Linux Masque',
      properties: {
        masque_texts: {
          title: 'Texts',
          type: 'array',
          uniqueItems: true,
          items: {'type': 'string'},
          default: DEFAULT_MASQUES.linux.texts,
          description: 'List of masque strings that will be applied to the Linux Agent binary.'
        },
        masque_base64: {
          title: 'Base64',
          type: 'array',
          uniqueItems: true,
          items: {
            type: 'string',
            format: 'valid-base64'
          },
          maxItems: 1,
          default: DEFAULT_MASQUES.linux.base64,
          description: 'List of masque Base64 strings that will be applied to the Linux Agent binary.'
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
          items: {'type': 'string'},
          default: DEFAULT_MASQUES.windows.texts,
          description: 'List of masque strings that will be applied to the Windows Agent binary.'
        },
        masque_base64: {
          title: 'Base64',
          type: 'array',
          uniqueItems: true,
          items: {
            type: 'string',
            format: 'valid-base64'
          },
          maxItems: 1,
          default: DEFAULT_MASQUES.windows.base64,
          description: 'List of masque Base64 strings that will be applied to the Linux Agent binary.'
        }
      }
    }
  }
}
