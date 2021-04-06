import React from 'react';
import PropTypes from 'prop-types';


export default function CommandSection(props){
  return (
    <div className={'command-section'}>
      {props.commands[0].name}
      {props.commands[0].command}
    </div>
  )
}

CommandSection.propTypes = {
  commands: PropTypes.arrayOf(PropTypes.exact({
    name: PropTypes.string,
    command: PropTypes.string
  }))
}
