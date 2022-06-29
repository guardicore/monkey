import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';

export default function UiSchema(props) {
  const UiSchema = {
    propagation: {
      'ui:order': ['exploitation', 'maximum_depth', 'network_scan'],
      exploitation: {
        brute_force: {
          'ui:widget': AdvancedMultiSelect
        },
        vulnerability: {
          'ui:widget': AdvancedMultiSelect
        }
      },
      network_scan: {
        targets: {
          info_box: {
            'ui:field': InfoBox
          }
        }
      }
    }
  };
  return UiSchema[props.selectedSection]
}
