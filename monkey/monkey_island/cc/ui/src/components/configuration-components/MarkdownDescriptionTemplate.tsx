import {DescriptionFieldProps} from '@rjsf/utils';
import React from 'react';
import ReactMarkdown from 'react-markdown';


function MarkdownDescriptionTemplate(props: DescriptionFieldProps) {
  const {description, id} = props;
  return (
    <ReactMarkdown linkTarget={'_blank'}
                   className={'markdown'} >
      {description.toString()}
    </ReactMarkdown>
  );
}

export default MarkdownDescriptionTemplate;
