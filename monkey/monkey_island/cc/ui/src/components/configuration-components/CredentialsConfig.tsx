import Form from '@rjsf/bootstrap-4';
import React from 'react';
import _ from 'lodash';
import validator from '@rjsf/validator-ajv8';

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
          validator={validator}
          onChange={(formData) => {onChange(formData.formData)}}
          // @ts-ignore
          customFormats={customFormats}
          className={className}
          liveValidate
    children={true}/>
  </>)
}
