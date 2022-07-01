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
            classNames: 'config-template-no-header'
          }
        },
        vulnerability: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect,
          vulnerability_classes: {
            classNames: 'config-template-no-header'
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
    },
    credential_collectors: {
      collectors: {
        classNames: 'config-template-no-header',
        'ui:widget': AdvancedMultiSelect,
        credential_collectors_classes :{
          classNames: 'config-template-no-header'
        }
      }
    }
  };
  return UiSchema[props.selectedSection]
}
