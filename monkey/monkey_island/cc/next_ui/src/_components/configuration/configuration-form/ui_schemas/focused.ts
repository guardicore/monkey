import TabsTemplate from '@/_components/configuration/configuration-form/TabsTemplate';
import FocusedObjectFieldTemplate from '../FocusedView';

export const FocusedSchema = {
    'ui:ObjectFieldTemplate': TabsTemplate,
    'ui:submitButtonOptions': {
        norender: true
    },
    propagation: {
        'ui:ObjectFieldTemplate': FocusedObjectFieldTemplate
    },
    payloads: {},
    credentials_collectors: {},
    masquerade: {},
    polymorphism: {},
    advanced: {}
};
