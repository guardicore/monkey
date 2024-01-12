import React, { useState } from 'react';
import Form from '@rjsf/mui';
import { FocusedSchema } from './ui_schemas/focused';
import { SummarySchema } from './ui_schemas/summary';
import FocusedObjectFieldTemplate from './FocusedView';

type ConfigurationFormProps = {
    schema: any;
    configuration: any;
    validator: any;
};

// schema is the UI-formatted schema
// configuration is the UI-formatted configuration
const ConfigurationForm = ({
    schema,
    configuration,
    validator
}: ConfigurationFormProps) => {
    const [uiSchema, setUiSchema] = useState(SummarySchema);
    const [additionalProps, setAdditionalProps] = useState({});
    const [selectedPath, setSelectedPath] = useState('');
    const navChanged = (path: string) => {
        console.log('navChanged: ', path);
        if (path.includes('.')) {
            console.log('focusedView');
            focusedView();
        } else {
            console.log('summaryView');
            summaryView();
        }
        setSelectedPath(path);
        // Change the view based on the path
        // - Summary view
        // - Focused view
    };
    const summaryView = () => {
        setUiSchema(SummarySchema);
        setAdditionalProps({});
    };
    const focusedView = () => {
        setUiSchema(FocusedSchema);
        setAdditionalProps({ ObjectFieldTemplate: FocusedObjectFieldTemplate });
    };

    return (
        <Form
            schema={schema}
            formData={configuration}
            validator={validator}
            uiSchema={uiSchema}
            formContext={{
                rootSchema: schema,
                onNavChanged: navChanged,
                selectedPath: selectedPath
            }}
            liveValidate={true}
            {...additionalProps}
        />
    );
};

// Create a redux slice for configuration...
// - Define reducer, actions
// Add the slice to the store
// May be able to use mapStateToProps and mapDispatchToProps to provide the configuration to the components
// - mapStateToProps can *and should* reshape the data for the component
//   - Probably won't make use of this since we're using RJSF...? At least not for plugins
// - Seems to prevent the use of slices.
// - Use mapDispatchToProps to provide the actions to the component
// - Use the connect function to connect the component to the store, providing the mapStateToProps and mapDispatchToProps
//
// For the purposes of the ConfigurationForm, this applies only to the configuration data
//
// Note:
// - JSONSchema is for rendering
// - UiSchema is for specifying specific controls for rendering
//
// How is RJSF used in the old UI?
// - Uses multiple rjsf Form components, one for each section
//   - Provides the JSONSchema sub-schema for the selected section (schema)
//   - Provides the UiSchema sub-schema for the selected section (fullUiSchema)
//   - Provides the sub configuration for the selected section (formData)
//   - Provides and onChange handler that applies the config for the selected section (onChange)
// - Renders each section in a tab, depending on the selected section
// - Uses specialized forms for the Propagation and Masquerade sections
//   - Propagation has subtabs
//   - Masquerade uses a copy of the Masquerade strings
// - Uses a custom template for the PluginSelector
//
// How should RJSF be used in the new UI?
// - Can we render tabs without using a specialized form?
//   - We probably need a top-level form for rendering the tabs
//     - Can probably use a custom template for this as well
//   - We may not need to render tabs for the Propagation section
// - How can we render a top-level view of the configuration?
//   - This is likely easier than rendering
// - How can we provide separate screens for drilling down into the configuration?
//   - This is likely easier than rendering
// - How can we provide a specialized form for plugins?
//   - We use a UiSchema to specify how certain fields are rendered
//
// Note:
// - The whole point of the UI is to edit the configuration
//   - Therefore it need not ALL be RJSF
//   - In fact, it may be best to use RJSF only for the plugins, as long as we can still validate easily
// - RJSF is meant to make it easy to display the configuration (at least the plugins)
// - Could probably use RJSF, and swap out the UiSchema based on whether we want summary or detailed view
// - Need to install plugins, then reload the config/schema in order to display/configure them

// Configuration
// - Tabs view component
// - Note: Will probably want a summary and detailed view for each
//   - Don't display plugin settings in the summary view..., just enabled plugins
//   - Show errors by section?
// - Propagation component
//   - To display subsections
// - A plugin selector component
// - An orderable chips component
// - ...

// TODO:
// - Figure out if one can navigate / breadcrumb without clearing the form
//  - May be able to use shallow routing https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating#shallow-routing
//  - However, may not need to navigate if we're using a breadcrumb

export default ConfigurationForm;
