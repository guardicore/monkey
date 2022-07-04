import AdvancedMultiSelect from '../ui-components/AdvancedMultiSelect';
import InfoBox from './InfoBox';
import TextBox from './TextBox.js';

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
              classNames: 'config-template-no-header'
            }
          }
        }
      },
      network_scan: {
        targets: {
          info_box: {
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
        fingerprinters:{
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
        info_box : {
          'ui:field': InfoBox
        },
        text_box: {
          'ui:field': TextBox
        }
      }
    },
    custom_pbas: {
      classNames: 'config-template-no-header'
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
