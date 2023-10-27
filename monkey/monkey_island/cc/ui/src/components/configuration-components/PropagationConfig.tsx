import Form from '@rjsf/bootstrap-4';
import React, {useState} from 'react';
import {Nav} from 'react-bootstrap';
import _ from 'lodash';
import CredentialPairs from '../ui-components/credential-pairs/CredentialPairs';

const sectionOrder = [
  'exploitation',
  'network_scan',
  'credentials',
  'general'
];

const initialSection = sectionOrder[0];

export const EXPLOITERS_PATH_PROPAGATION = 'exploitation.exploiters';
export const EXPLOITERS_CONFIG_PATH = 'propagation.' + EXPLOITERS_PATH_PROPAGATION;

export const FINGERPRINTERS_PATH_PROPAGATION = 'network_scan.fingerprinters';
export const FINGERPRINTERS_CONFIG_PATH = 'propagation.' + FINGERPRINTERS_PATH_PROPAGATION;

export default function PropagationConfig(props) {
  const {
    schema,
    fullUiSchema,
    onChange,
    customFormats,
    className,
    configuration,
    credentials,
    onCredentialChange,
    selectedPlugins,
    setSelectedPlugins,
    selectedConfigSection,
    validator,
    transformErrors
  } = props;

  const [selectedSection, setSelectedSection] = useState(initialSection);
  const [propagationUiSchema, setPropagationUiSchema] = useState(fullUiSchema);

  const onFormDataChange = (formData) => {
    let formDataClone = _.clone(formData.formData);
    let configurationClone = _.clone(configuration);

    configurationClone[selectedSection] = formDataClone;
    onChange(configurationClone);
  }

  const setUiSchemaForCurrentSection = (uiSubschema, path) => {
    let newSchema = _.cloneDeep(propagationUiSchema);
    _.set(newSchema, path, uiSubschema);
    setPropagationUiSchema(newSchema);
  }

  const renderNav = () => {
    return (<Nav variant="tabs"
                 fill
                 activeKey={selectedSection} onSelect={setSelectedSection}
                 style={{'marginBottom': '2em'}}
                 className={'config-nav'}>
      {sectionOrder.map(section => {
        return (
          <Nav.Item key={section}>
            <Nav.Link eventKey={section}>{getNavTitle(schema, section)}</Nav.Link>
          </Nav.Item>);
      })}
    </Nav>)
  }

  const getForm = () => {
    let displayedSchema = getSchemaByKey(schema, selectedSection);
    let displayedUiSchema = getUiSchemaByKey(propagationUiSchema, selectedSection);
    if (selectedSection === 'credentials') {
      return <CredentialPairs onCredentialChange={onCredentialChange}
                              transformErrors={transformErrors}
                              credentials={credentials} />
    } else {
      let selectedSectionData = configuration[selectedSection];
      let selectedConfigPlugins = selectedPlugins[selectedConfigSection];
      if(selectedConfigSection === 'propagation'){
        selectedConfigPlugins = selectedConfigPlugins[selectedSection];
      }
      return <Form schema={displayedSchema}
                   uiSchema={displayedUiSchema}
                   formData={selectedSectionData}
                   validator={validator}
                   onChange={onFormDataChange}
                   // @ts-ignore
                   customFormats={customFormats}
                   className={className}
                   // Each form must be a unique component
                   // which is defined by the selectedSection
                   key={selectedSection}
                   liveValidate
                   // children={true} hides the submit button
                   children={true}
                   formContext={{
                     'selectedPlugins': selectedConfigPlugins,
                     'setSelectedPlugins': setSelectedPlugins,
                     'section': selectedConfigSection,
                     'subSection': selectedSection,
                     setUiSchema: setUiSchemaForCurrentSection
                   }}/>
    }
  }

  return (<div>
    {renderNav()}
    {getForm()}
  </div>)
}

function getSchemaByKey(schema, key) {
  return schema['properties'][key];
}

function getUiSchemaByKey(uiSchema, key) {
  return uiSchema[key];
}

function getNavTitle(schema, key) {
  return schema['properties'][key].title;
}
