import CheckboxWithMessage from './CheckboxWithMessage';
import SensitiveTextInput from '../ui-components/SensitiveTextInput';
import SensitiveTextareaInput from '../ui-components/SensitiveTextareaInput';
import PluginSelectorTemplate from './PluginSelectorTemplate';
import ArrayFieldTitleTemplate from './ArrayFieldTitleTemplate';

export default function UiSchema(props) {
  const UiSchema = {
    propagation: {
      exploitation: {
        exploiters: {
          'ui:ObjectFieldTemplate': PluginSelectorTemplate
        }
      },
      credentials: {
        exploit_password_list: {
          items: {
            'ui:widget': SensitiveTextInput
          }
        },
        exploit_lm_hash_list: {
          items: {
            'ui:widget': SensitiveTextInput
          }
        },
        exploit_ntlm_hash_list: {
          items: {
            'ui:widget': SensitiveTextInput
          }
        },
        exploit_ssh_keys: {
          items: {
            'ui:TitleFieldTemplate': ArrayFieldTitleTemplate,
            public_key: {
              'ui:widget': 'TextareaWidget'
            },
            private_key: {
              'ui:widget': SensitiveTextareaInput
            }
          }
        }
      },
      network_scan: {
        targets: {
          blocked_ips: {
            items: {
              'ui:classNames': 'config-template-no-header'
            }
          },
          inaccessible_subnets: {
            items: {
              'ui:classNames': 'config-template-no-header'
            }
          },
          scan_my_networks: {
            'ui:widget': CheckboxWithMessage
          },
          subnets: {
            items: {
              'ui:classNames': 'config-template-no-header'
            }
          }
        },
        tcp: {
          ports: {
            items: {
              'ui:classNames': 'config-template-no-header'
            }
          }
        },
        fingerprinters: {
          'ui:widget': 'hidden'
        }
      }
    },
    payloads: {
      'ui:ObjectFieldTemplate': PluginSelectorTemplate
    },
    credentials_collectors: {
      'ui:ObjectFieldTemplate': PluginSelectorTemplate
    },
    masquerade: {
      linux: {
        masque_base64: {
          'ui:widget': 'textarea',
          'ui:options': {
            rows: 3
          }
        }
      },
      windows: {
        masque_base64: {
          'ui:widget': 'textarea',
          'ui:options': {
            rows: 3
          }
        }
      }
    },
    polymorphism: {
      randomize_agent_hash: {
        'ui:widget': CheckboxWithMessage
      }
    }
  };
  return UiSchema[props.selectedSection]
}
