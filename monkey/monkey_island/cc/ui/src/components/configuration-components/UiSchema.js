import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';
import TextBox from './TextBox.js';
import WarningBox from './WarningBox';
import SensitiveTextInput from '../ui-components/SensitiveTextInput';
import PluginSelectorTemplate from './PluginSelectorTemplate';

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
            public_key: {
              'ui:widget': 'TextareaWidget'
            },
            private_key: {
              'ui:widget': 'TextareaWidget'
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
          info_box_scan_my_networks: {
            'ui:field': WarningBox
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
          'ui:widget': AdvancedMultiSelect,
          fingerprinter_classes: {
            'ui:classNames': 'config-template-no-header'
          }
        }
      }
    },
    payloads: {
      encryption: {
        info_box: {
          'ui:field': InfoBox
        },
        file_extension: {
          'ui:emptyValue': ''
        },
        directories: {
          // Directory inputs are dynamically hidden
        },
        text_box: {
          'ui:field': TextBox
        },
        enabled: {
          'ui:widget': 'hidden'
        }
      },
      other_behaviors: {
        'ui:widget': 'hidden'
      }
    },
    credential_collectors: {
      'ui:widget': AdvancedMultiSelect,
      credential_collectors_classes: {
        'ui:classNames': 'config-template-no-header'
      }
    }
  };
  return UiSchema[props.selectedSection]
}
