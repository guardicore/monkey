import Form from '@rjsf/bootstrap-4';
import React from 'react';
import _ from 'lodash';

export default function CredentialsConfig(props) {
  const {
    schema,
    uiSchema,
    credentials,
    onChange,
    customFormats,
    className,
    validator,
    transformErrors
  } = props;

  let credentialsCopy = _.clone(credentials);
  return (<>
    <Form schema={schema}
          uiSchema={uiSchema}
          formData={credentialsCopy}
          validator={validator}
          transformErrors={transformErrors}
          onChange={(formData) => {onChange(formData.formData)}}
          // @ts-ignore
          customFormats={customFormats}
          className={className}
          liveValidate
    children={true}/>
  </>)
}
