import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';

export default function UiSchema(props) {
  const UiSchema = {
    propagation: {
      exploitation: {
        brute_force: {
          brute_force_classes: {
            classNames: 'config-template-no-header',
            'ui:widget': AdvancedMultiSelect
          }
        },
        vulnerability: {
          vulnerability_classes: {
            classNames: 'config-template-no-header',
            'ui:widget': AdvancedMultiSelect
          }
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
