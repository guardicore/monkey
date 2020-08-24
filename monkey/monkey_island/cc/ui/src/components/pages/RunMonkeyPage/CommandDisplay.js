import {Button, Card, Nav} from 'react-bootstrap';
import CopyToClipboard from 'react-copy-to-clipboard';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClipboard} from '@fortawesome/free-solid-svg-icons/faClipboard';
import React, {useState} from 'react';
import PropTypes from 'prop-types';

export default function commandDisplay(props) {

  const [selectedVariant, setSelectedVariant] = useState(props.commands[0].name);

  function renderNav() {
    return (
      <Nav variant='pills' fill activeKey={selectedVariant} onSelect={setSelectedVariant}>
        {props.commands.map(command => {
          return (
            <Nav.Item key={command.name}>
              <Nav.Link eventKey={command.name}>{command.name}</Nav.Link>
            </Nav.Item>);
        })}
      </Nav>);
  }

  function getCommandByName(name, commands) {
    commands.forEach((command) => {

    })
  }

  return (
    <>
      {renderNav()}
      <Card style={{'margin': '0.5em'}}>
        <div style={{'overflow': 'auto', 'padding': '0.5em'}}>
          <CopyToClipboard text={props.commands[0].name} className="pull-right btn-sm">
            <Button style={{margin: '-0.5em'}} title="Copy to Clipboard">
              <FontAwesomeIcon icon={faClipboard}/>
            </Button>
          </CopyToClipboard>
          <code>{props.commands[0].command}</code>
        </div>
      </Card>
    </>
  )
}

commandDisplay.propTypes = {
  commands: PropTypes.arrayOf(PropTypes.exact({
    name: PropTypes.string,
    command: PropTypes.string
  }))
}
