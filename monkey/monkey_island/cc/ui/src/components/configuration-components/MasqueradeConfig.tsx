import Form from '@rjsf/bootstrap-4';
import React from 'react';
import _ from 'lodash';

export default function MasqueradeConfig(props) {
  const {
    schema,
    fullUiSchema,
    masqueStrings,
    onChange,
    customFormats,
    className,
    validator,
    transformErrors
  } = props;

  let masqueStringsCopy = _.clone(masqueStrings);

  return <>
    <Form schema={schema}
          uiSchema={fullUiSchema}
          formData={masqueStringsCopy}
          validator={validator}
          transformErrors={transformErrors}
          onChange={(formData) => {
            onChange(formData.formData)
          }}
          // @ts-ignore
          customFormats={customFormats}
          className={className}
          liveValidate
          children={true}
    />
  </>
}
