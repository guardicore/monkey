import TabsTemplate from '@/_components/configuration/configuration-form/TabsTemplate';
import SummaryObjectFieldTemplate from '@/_components/configuration/configuration-form/Summary';

export const SummarySchema = {
    'ui:ObjectFieldTemplate': TabsTemplate,
    'ui:submitButtonOptions': {
        norender: true
    },
    propagation: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    },
    payloads: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    },
    credentials_collectors: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    },
    masquerade: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    },
    polymorphism: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    },
    advanced: {
        'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
    }
};
