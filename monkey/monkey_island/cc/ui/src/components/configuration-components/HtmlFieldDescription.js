import React from 'react';

function HtmlFieldDescription(props) {
  var content_obj = {__html: props.description};
  return <p id={props.id} className='field-description' dangerouslySetInnerHTML={content_obj} />;
}

export default HtmlFieldDescription;
