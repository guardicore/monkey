import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';

export default function UiSchema(props) {
  const UiSchema = {
    propagation: {
      exploitation: {
        brute_force: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect,
          brute_force_classes: {
            classNames: 'config-template-no-header',
          }
        },
        vulnerability: {
          classNames: 'config-template-no-header',
          vulnerability_classes: {
            classNames: 'config-template-no-header',
            //'ui:widget': AdvancedMultiSelect
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
