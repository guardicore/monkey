import {Button, Card, Nav} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClipboard} from '@fortawesome/free-solid-svg-icons/faClipboard';
import React, {useEffect, useState} from 'react';
import PropTypes from 'prop-types';

export default function commandDisplay(props) {

  const [selectedCommand, setSelectedCommand] = useState(props.commands[0]);

  function setSelectedCommandByName(type){
    setSelectedCommand(getCommandByName(props.commands, type));
  }

  function getCommandByName(commands, type){
    return commands.find((command) => {return command.type === type});
  }

  useEffect(() => {
    let sameTypeCommand = getCommandByName(props.commands, selectedCommand.type);
    if( sameTypeCommand !== undefined){
      setSelectedCommand(sameTypeCommand);
    } else {
      setSelectedCommand(props.commands[0]);
    }
  }, [props.commands]);

  function renderNav() {
    return (
      <Nav variant='pills' fill activeKey={selectedCommand.type} onSelect={setSelectedCommandByName}>
        {props.commands.map(command => {
          return (
            <Nav.Item key={command.type}>
              <Nav.Link eventKey={command.type}>{command.type}</Nav.Link>
            </Nav.Item>);
        })}
      </Nav>);
  }

  return (
    <>
      {renderNav()}
      <Card style={{'margin': '0.5em'}}>
        <div style={{'overflow': 'auto', 'padding': '0.5em'}}>
          <CopyToClipboard text={selectedCommand.type} className="pull-right btn-sm">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <FontAwesomeIcon icon={faClipboard}/>
            </Button>
          </CopyToClipboard>
          <code>{selectedCommand.command}</code>
        </div>
      </Card>
    </>
  )
}

commandDisplay.propTypes = {
  commands: PropTypes.arrayOf(PropTypes.exact({
    type: PropTypes.string,
    command: PropTypes.string
  }))
}
