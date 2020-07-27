import Form from 'react-jsonschema-form-bs4';
import React, {useState} from 'react';
import {Nav} from 'react-bootstrap';

const sectionOrder = [
  'network',
  'monkey',
  'island_server',
  'logging',
  'exploits',
  'dropper',
  'classes',
  'general',
  'kill_file',
  'testing'
];
const initialSection = sectionOrder[0];

export default function InternalConfig(props) {
  const {
    schema,
    uiSchema,
    onChange,
    customFormats,
    className,
    formData
  } = props;
  const [selectedSection, setSelectedSection] = useState(initialSection);
  const [displayedSchema, setDisplayedSchema] = useState(getSchemaByKey(schema, initialSection));
  const [displayedSchemaUi, setDisplayedSchemaUi] = useState(uiSchema[initialSection]);

  const onInnerDataChange = (innerData) => {
    formData[selectedSection] = innerData.formData;
    onChange({formData: formData});
  }

  const setSection = (sectionKey) => {
    setSelectedSection(sectionKey);
    setDisplayedSchema(getSchemaByKey(schema, sectionKey));
    setDisplayedSchemaUi(uiSchema[sectionKey]);
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
  let definitions = schema['definitions'];
  return {definitions: definitions, properties: schema['properties'][key]['properties']};
}

function getNavTitle(schema, key) {
  return schema.properties[key].title;
}
