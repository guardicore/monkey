import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import PbaInput from './PbaInput';
import {API_PBA_LINUX, API_PBA_WINDOWS} from '../pages/ConfigurePage';
import InfoBox from './InfoBox';
import TextBox from './TextBox';
import SensitiveTextInput from '../ui-components/SensitiveTextInput';

export default function UiSchema(props) {
  const UiSchema = {
    basic: {
      'ui:order': ['exploiters', 'credentials'],
      exploiters: {
        exploiter_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      },
      credentials: {
        exploit_user_list: {
          items: {
            classNames: 'config-template-no-header'
          }
        },
        exploit_password_list: {
          items: {
            classNames: 'config-template-no-header',
            'ui:widget': SensitiveTextInput
          }
        }
      }
    },
    basic_network: {
      'ui:order': ['scope', 'network_analysis'],
      scope: {
        info_box: {
          'ui:field': InfoBox
        },
        blocked_ips: {
          items: {
            classNames: 'config-template-no-header'
          }
        },
        subnet_scan_list: {
          format: 'ip-list',
          items: {
            classNames: 'config-template-no-header'
          }
        }
      },
      network_analysis: {
        inaccessible_subnets: {
          items: {
            classNames: 'config-template-no-header'
          }
        }
      }
    },
    monkey: {
      post_breach: {
        post_breach_actions: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        },
        custom_PBA_linux_cmd: {
          'ui:widget': 'textarea',
          'ui:emptyValue': ''
        },
        PBA_linux_file: {
          'ui:widget': PbaInput,
          'ui:options': {
            filename: props.PBA_linux_filename,
            apiEndpoint: API_PBA_LINUX,
            setPbaFilename: props.setPbaFilenameLinux
          }
        },
        custom_PBA_windows_cmd: {
          'ui:widget': 'textarea',
          'ui:emptyValue': ''
        },
        PBA_windows_file: {
          'ui:widget': PbaInput,
          'ui:options': {
            filename: props.PBA_windows_filename,
            apiEndpoint: API_PBA_WINDOWS,
            setPbaFilename: props.setPbaFilenameWindows
          }
        },
        PBA_linux_filename: {
          classNames: 'linux-pba-file-info',
          'ui:emptyValue': ''
        },
        PBA_windows_filename: {
          classNames: 'windows-pba-file-info',
          'ui:emptyValue': ''
        }
      },
      credential_collectors: {
        credential_collector_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    },
    ransomware: {
      encryption: {
        info_box: {
          'ui:field': InfoBox
        },
        directories: {
            // Directory inputs are dynamically hidden
        },
        text_box: {
          'ui:field': TextBox
        },
      enabled: {'ui:widget': 'hidden'}
      },
      other_behaviors : {'ui:widget': 'hidden'}
    },
    internal: {
      classes: {
        finger_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      },
      exploits: {
        exploit_lm_hash_list:{
          items: {
              'ui:widget': SensitiveTextInput
          }
        },
        exploit_ntlm_hash_list: {
          items: {
              'ui:widget': SensitiveTextInput
          }
        }
      }
    }
  };
  return UiSchema[props.selectedSection]
}
