import React from 'react';

function ArrayFieldTitleTemplate(props) {
  const { id, title } = props;
  const sequenceNumber = id.replace(/[^0-9]/g, '');
  return (
    <h5 id={id}>
      {title} {sequenceNumber}
    </h5>
  );
}

export default ArrayFieldTitleTemplate;
