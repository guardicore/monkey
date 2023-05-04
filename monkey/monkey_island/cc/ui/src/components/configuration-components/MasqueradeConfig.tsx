import Form from '@rjsf/bootstrap-4';
import React from 'react';
import _ from 'lodash';
import validator from '@rjsf/validator-ajv8';

export default function MasqueradeConfig(props) {
  const {
    schema,
    uiSchema,
    masqueList,
    onChange,
    customFormats,
    className
  } = props;

  let masqueListCopy = _.clone(masqueList);
  return (<>
    <Form schema={schema}
          uiSchema={uiSchema}
          formData={masqueListCopy}
          validator={validator}
          onChange={(formData) => {onChange(formData.formData)}}
          // @ts-ignore
          customFormats={customFormats}
          className={className}
          liveValidate
    children={true}/>
  </>)
}
