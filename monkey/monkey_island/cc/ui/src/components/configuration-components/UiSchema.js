import AdvancedMultiSelect from "../ui-components/AdvancedMultiSelect";
import PbaInput from "./PbaInput";
import {API_PBA_LINUX, API_PBA_WINDOWS} from '../pages/ConfigurePage';

export default function UiSchema(props) {
  const UiSchema = {
    basic: {
      'ui:order': ['general', 'credentials'],
    },
    basic_network: {},
    monkey: {
      behaviour: {
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
      }
    },
    cnc: {},
    network: {},
    exploits: {
      general: {
        exploiter_classes: {
          'ui:widget': AdvancedMultiSelect,
          'ui:options': {
            defaultPaneParams: {
              title: 'Exploiters',
              content: 'Click on exploiter to get more information about it.'
            }
          }
        }
      }
    },
    internal: {
      general: {
        started_on_island: {'ui:widget': 'hidden'}
      }
    }
  }
  return UiSchema[props.selectedSection]
}
