import Form from '@rjsf/bootstrap-4';
import React from 'react';
import _ from 'lodash';
import validator from '@rjsf/validator-ajv8';

export default function MasqueradeConfig(props) {
  const {
    schema,
    uiSchema,
    masqueStrings,
    onMasqueStringsChange,
    customFormats,
    className
  } = props;

  let masqueStringsCopy = _.clone(masqueStrings);
  return (<>
    <Form schema={schema}
          uiSchema={uiSchema}
          formData={masqueStringsCopy}
          validator={validator}
          onChange={(formData) => {onMasqueStringsChange(formData.formData)}}
          // @ts-ignore
          customFormats={customFormats}
          className={className}
          liveValidate
    children={true}/>
  </>)
}
