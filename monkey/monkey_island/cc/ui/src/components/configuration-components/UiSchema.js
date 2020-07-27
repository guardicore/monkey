import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import PbaInput from './PbaInput';
import {API_PBA_LINUX, API_PBA_WINDOWS} from '../pages/ConfigurePage';
import FieldWithInfo from './FieldWithInfo';

export default function UiSchema(props) {
  const UiSchema = {
    basic: {
      'ui:order': ['exploiters', 'credentials'],
      exploiters: {
        exploiter_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    },
    basic_network: {
      'ui:order': ['scope', 'network_analysis'],
      scope: {
        blocked_ips: {
          'ui:field': FieldWithInfo
        },
        subnet_scan_list: {
          format: 'ip-list'
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
      system_info: {
        system_info_collector_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    },
    internal: {
      general: {
        started_on_island: {'ui:widget': 'hidden'}
      },
      classes: {
        finger_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      },
      monkey: {
        alive: {
          classNames: 'config-field-hidden'
        }
      }
    }
  };
  return UiSchema[props.selectedSection]
}
