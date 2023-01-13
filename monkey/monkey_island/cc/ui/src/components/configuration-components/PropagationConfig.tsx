import Form from '@rjsf/bootstrap-4';
import React, {useEffect, useState} from 'react';
import {Nav} from 'react-bootstrap';
import _ from 'lodash';
import CredentialsConfig from './CredentialsConfig';
import validator from '@rjsf/validator-ajv8';

const sectionOrder = [
  'exploitation',
  'network_scan',
  'credentials',
  'general'
];

const initialSection = sectionOrder[0];

export const EXPLOITERS_PATH_PROPAGATION = 'exploitation.exploiters';
export const EXPLOITERS_CONFIG_PATH = 'propagation.' + EXPLOITERS_PATH_PROPAGATION;

export default function PropagationConfig(props) {
  const {
    schema,
    uiSchema,
    onChange,
    customFormats,
    className,
    configuration,
    credentials,
    onCredentialChange,
    exploiters
  } = props;


  // rjsf component automatically creates an instance from the defaults in the schema
  // https://github.com/rjsf-team/react-jsonschema-form/issues/2980
  // we don't want that, because we won't know which plugins were enabled
  const [selectedSection, setSelectedSection] = useState(initialSection);
  const [selectedExploiters, setSelectedExploiters] = useState(exploiters);

  useEffect(() => onFormDataChange(configuration[selectedSection]),
    [selectedExploiters]);

  const onFormDataChange = (formData) => {
    let formDataClone = _.cloneDeep(formData.formData);
    let configurationClone = _.cloneDeep(configuration);

    configurationClone[selectedSection] = formDataClone;
    _.set(configurationClone, EXPLOITERS_PATH_PROPAGATION, selectedExploiters)
    onChange(configurationClone);
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
    let displayedUiSchema = getUiSchemaByKey(uiSchema, selectedSection);
    if (selectedSection === 'credentials') {
      return <CredentialsConfig schema={displayedSchema}
                                uiSchema={displayedUiSchema}
                                credentials={credentials}
                                onChange={onCredentialChange}
                                customFormats={customFormats}
                                className={className}/>
    } else {
      let selectedSectionData = configuration[selectedSection];
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
                   formContext={{'selectedExploiters': selectedExploiters,
                   'setSelectedExploiters': setSelectedExploiters}}/>
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
