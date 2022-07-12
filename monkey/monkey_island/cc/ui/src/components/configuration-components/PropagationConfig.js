import Form from 'react-jsonschema-form-bs4';
import React, {useState} from 'react';
import {Nav} from 'react-bootstrap';
import {CREDENTIALS} from '../../services/configuration/credentials.js';

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
    formData
  } = props;
  console.log(schema, uiSchema, formData);
  const [selectedSection, setSelectedSection] = useState(initialSection);
  const [displayedSchema, setDisplayedSchema] = useState(getSchemaByKey(schema, initialSection));
  const [displayedSchemaUi, setDisplayedSchemaUi] = useState(getUiSchemaByKey(uiSchema, initialSection));
  const onInnerDataChange = (innerData) => {
    console.log(innerData);
    formData[selectedSection] = innerData.formData;
    onChange({formData: formData});
  }

  const setSection = (sectionKey) => {
    console.log(sectionKey);
    setSelectedSection(sectionKey);
    setDisplayedSchema(getSchemaByKey(schema, sectionKey));
    setDisplayedSchemaUi(getUiSchemaByKey(uiSchema, sectionKey));
  }

  const renderNav = () => {
    return (<Nav variant='tabs'
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

  console.log(displayedSchemaUi)

  return (<div>
    {renderNav()}
    <Form schema={displayedSchema}
          uiSchema={displayedSchemaUi}
          formData={formData[selectedSection]}
          onChange={onInnerDataChange}
          customFormats={customFormats}
          className={className}
          liveValidate>
      <button type='submit' className={'hidden'}>Submit</button>
    </Form>
  </div>)
}

function getSchemaByKey(schema, key) {
  if(key === 'maximum_depth'){
    return schema['properties'][key];
  }
  if(key === 'credentials') {
    return { properties: CREDENTIALS['properties']};
  }
  let definitions = schema['definitions'];

  return {definitions: definitions, properties: schema['properties'][key]['properties']};
}


function getUiSchemaByKey(uiSchema, key){
  return uiSchema[key];
}

function getNavTitle(schema, key) {
  if(key === 'maximum_depth'){
    return 'General';
  }
  if(key === 'credentials'){
    return 'Credentials';
  }
  return schema.properties[key].title;
}
