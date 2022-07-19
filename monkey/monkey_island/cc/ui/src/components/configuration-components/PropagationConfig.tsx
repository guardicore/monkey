import Form from 'react-jsonschema-form-bs4';
import React, {useState, useEffect} from 'react';
import {Nav} from 'react-bootstrap';
import _ from 'lodash';
import CredentialsConfig from './CredentialsConfig';
import AuthComponent from '../AuthComponent';

const sectionOrder = [
  'exploitation',
  'network_scan',
  'credentials',
  'maximum_depth'
];

const initialSection = sectionOrder[0];

export default function PropagationConfig(props) {
  const {
    schema,
    uiSchema,
    onChange,
    customFormats,
    className,
    configuration,
    credentials,
    onCredentialChange
  } = props;
  const [selectedSection, setSelectedSection] = useState(initialSection);

  const onFormDataChange = (formData) => {
    let formDataClone = _.clone(formData.formData);
    let configurationClone = _.clone(configuration);

    configurationClone[selectedSection] = formDataClone;
    onChange(configurationClone);
  }

  const setSection = (sectionKey) => {
    setSelectedSection(sectionKey);
  }

  const renderNav = () => {
    return (<Nav variant="tabs"
                 fill
                 activeKey={selectedSection} onSelect={setSection}
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
    let selectedSectionData = configuration[selectedSection];
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
      let formForm = <Form schema={displayedSchema}
                   uiSchema={displayedUiSchema}
                   formData={selectedSectionData}
                   onChange={onFormDataChange}
                   customFormats={customFormats}
                   className={className}
                   key={selectedSection}
                   liveValidate
                   // children={true} hides the submit button
                   children={true}/>
      return formForm;
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
  if (key === 'maximum_depth') {
    return 'General';
  }
  return schema['properties'][key].title;
}
