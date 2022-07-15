import Form from 'react-jsonschema-form-bs4';
import React, {useState, useEffect} from 'react';
import {Nav} from 'react-bootstrap';
import _ from 'lodash';
import CredentialsConfig from './CredentialsConfig';

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
  const [displayedSchema, setDisplayedSchema] = useState(getSchemaByKey(schema, initialSection));
  const [displayedSchemaUi, setDisplayedSchemaUi] = useState(getUiSchemaByKey(uiSchema, initialSection));
  const [localFormData, setLocalFormData] = useState(configuration[initialSection]);

  useEffect(() => {
    setLocalFormData(configuration[selectedSection]);
    setDisplayedSchema(getSchemaByKey(schema, selectedSection));
    setDisplayedSchemaUi(getUiSchemaByKey(uiSchema, selectedSection));
  }, [selectedSection])

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
    if (selectedSection === 'credentials') {
      return <CredentialsConfig schema={displayedSchema}
                                uiSchema={displayedSchemaUi}
                                credentials={credentials}
                                onChange={onCredentialChange}
                                customFormats={customFormats}
                                className={className}/>
    } else {
      return <Form schema={displayedSchema}
                   uiSchema={displayedSchemaUi}
                   formData={localFormData}
                   onChange={onFormDataChange}
                   customFormats={customFormats}
                   className={className}
                   liveValidate
                   // children={true} hides the submit button
                   children={true}/>
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
