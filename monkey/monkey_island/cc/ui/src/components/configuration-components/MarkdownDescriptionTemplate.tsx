import {DescriptionFieldProps} from '@rjsf/utils';
import React from 'react';
import remarkBreaks from 'remark-breaks';
import ReactMarkdown from 'react-markdown';


function MarkdownDescriptionTemplate(props: DescriptionFieldProps) {
  const {description, id} = props;
  return (
    <ReactMarkdown plugins={[remarkBreaks]}
                   linkTarget={'_blank'}
                   className={'markdown'}
                   children={description}/>
  );
}

export default MarkdownDescriptionTemplate;
