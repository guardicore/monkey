import Form from '@rjsf/bootstrap-4';
import React, {useState} from 'react';
import _ from 'lodash';


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
    if(path !== selectedSection){
      _.set(newSchema, path, uiSubschema);
      setFormUiSchema(newSchema);
    }else {
      setFormUiSchema(uiSubschema);
    }
  }
    const getForm = () => {
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
