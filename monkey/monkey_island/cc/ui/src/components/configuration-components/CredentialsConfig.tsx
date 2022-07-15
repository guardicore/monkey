import Form from 'react-jsonschema-form-bs4';
import React from 'react';
import _ from 'lodash';

export default function CredentialsConfig(props) {
  const {
    schema,
    uiSchema,
    credentials,
    onChange,
    customFormats,
    className
  } = props;

  let credentialsCopy = _.clone(credentials);

  return (<>
    <Form schema={schema}
          uiSchema={uiSchema}
          formData={credentialsCopy}
          onChange={(formData) => {onChange(formData.formData)}}
          customFormats={customFormats}
          className={className}
          liveValidate
    children={true}/>
  </>)
}
