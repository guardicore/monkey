import Form from '@rjsf/bootstrap-4';
import React, {useState} from 'react';
import _ from 'lodash';


export const EXPLOITERS_PATH_PROPAGATION = 'exploitation.exploiters';
export const EXPLOITERS_CONFIG_PATH = 'propagation.' + EXPLOITERS_PATH_PROPAGATION;

export default function FormConfig(props) {
  const {
    fullUiSchema,
    selectedPlugins,
    setSelectedPlugins,
    selectedSection
  } = props;

  const [formUiSchema, setFormUiSchema] = useState(fullUiSchema);

  const setUiSchemaForCurrentSection = (uiSubschema, path) => {
    let newSchema = _.cloneDeep(formUiSchema);
    _.set(newSchema, path, uiSubschema)
    setFormUiSchema(newSchema);
  }
    const getForm = () => {
        console.log(formUiSchema, fullUiSchema, selectedPlugins);
        return <Form {...props}
                 uiSchema={formUiSchema}
                 formContext={{
                   'selectedPlugins': selectedPlugins,
                   'setSelectedPlugins': setSelectedPlugins,
                   'setUiSchema': setUiSchemaForCurrentSection,
                   'section': selectedSection
                 }}>
                 <button type='submit' className={'hidden'}>Submit</button>
             </Form>
    }
  return (<div>
    {getForm()}
  </div>)
}
