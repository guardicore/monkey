import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';
import TextBox from './TextBox.js';
import PbaInput from './PbaInput';
import { API_PBA_LINUX, API_PBA_WINDOWS } from '../pages/ConfigurePage';
import SensitiveTextInput from '../ui-components/SensitiveTextInput';

export default function UiSchema(props) {
  const UiSchema = {
    propagation: {
      exploitation: {
        brute_force: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect,
          brute_force_classes: {
            classNames: 'config-template-no-header'
          }
        },
        vulnerability: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect,
          vulnerability_classes: {
            classNames: 'config-template-no-header'
          }
        },
        options: {
          http_ports: {
            items: {
            }
          }
        }
      },
      credentials: {
        exploit_ssh_keys: {
          items: {
            public_key: {
            },
            private_key: {
            }
          }
        },
        exploit_password_list: {
          items: {
            classNames: 'config-template-no-header',
            'ui:widget': SensitiveTextInput
          }
        },
        exploit_lm_hash_list: {
          items: {
            classNames: 'config-template-no-header',
            'ui:widget': SensitiveTextInput
          }
        },
        exploit_ntlm_hash_list: {
          items: {
            classNames: 'config-template-no-header',
            'ui:widget': SensitiveTextInput
          }
        }
      },
      network_scan: {
        targets: {
          info_box_general: {
            'ui:field': InfoBox
          },
          blocked_ips: {
            items: {
              classNames: 'config-template-no-header'
            }
          },
          inaccessible_subnets: {
            items: {
              classNames: 'config-template-no-header'
            }
          },
          info_box_scan_my_networks: {
            'ui:field': InfoBox
          },
          subnets: {
            items: {
              classNames: 'config-template-no-header'
            }
          }
        },
        tcp: {
          ports: {
            items: {
              classNames: 'config-template-no-header'
            }
          }
        },
        fingerprinters: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect,
          fingerprinter_classes: {
            classNames: 'config-template-no-header'
          }

        }
      }
    },
    payloads: {
      classNames: 'config-template-no-header',
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
    custom_pbas: {
      classNames: 'config-template-no-header',
      linux_command: {
        'ui:widget': 'textarea',
        'ui:emptyValue': ''
      },
      linux_file: {
        'ui:widget': PbaInput,
        'ui:options': {
          filename: props.linux_filename,
          apiEndpoint: API_PBA_LINUX,
          setPbaFilename: props.setPbaFilenameLinux
        }
      },
      windows_command: {
        'ui:widget': 'textarea',
        'ui:emptyValue': ''
      },
      windows_file: {
        'ui:widget': PbaInput,
        'ui:options': {
          filename: props.windows_filename,
          apiEndpoint: API_PBA_WINDOWS,
          setPbaFilename: props.setPbaFilenameWindows
        }
      },
      linux_filename: {
        classNames: 'linux-pba-file-info',
        'ui:emptyValue': ''
      },
      windows_filename: {
        classNames: 'windows-pba-file-info',
        'ui:emptyValue': ''
      }
    },
    post_breach_actions: {
      classNames: 'config-template-no-header',
      'ui:widget': AdvancedMultiSelect,
      post_breach_actions: {
        classNames: 'config-template-no-header'
      }
    },
    credential_collectors: {
      classNames: 'config-template-no-header',
      'ui:widget': AdvancedMultiSelect,
      credential_collectors_classes: {
        classNames: 'config-template-no-header'
      }
    }
  };
  return UiSchema[props.selectedSection]
}
