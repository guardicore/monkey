import { Button, Card, Nav } from "react-bootstrap";
import CopyToClipboard from "react-copy-to-clipboard";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClipboard } from "@fortawesome/free-solid-svg-icons/faClipboard";
import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

export default function commandDisplay(props) {
  const [selectedCommand, setSelectedCommand] = useState(props.commands[0]);

  function setSelectedCommandByName(type) {
    setSelectedCommand(getCommandByName(props.commands, type));
  }

  function getCommandByName(commands, type) {
    return commands.find((command) => {
      return command.type === type;
    });
  }

  useEffect(() => {
    let sameTypeCommand = getCommandByName(
      props.commands,
      selectedCommand.type,
    );
    if (sameTypeCommand !== undefined) {
      setSelectedCommand(sameTypeCommand);
    } else {
      setSelectedCommand(props.commands[0]);
    }
  }, [props.commands]);

  function handleKeyDown(event) {
    let charCode = String.fromCharCode(event.which).toLowerCase();
    if ((event.ctrlKey || event.metaKey) && charCode === "c") {
      props.onCopy();
    }
    if ((event.ctrlKey || event.metaKey) && charCode === "a") {
      event.preventDefault();
      let codeElement = event.target.querySelector("code");
      let selection = window.getSelection();
      let range = document.createRange();
      range.selectNode(codeElement);
      selection.addRange(range);
    }
    console.log(charCode);
  }

  function renderNav() {
    return (
      <Nav
        variant="tabs"
        activeKey={selectedCommand.type}
        onSelect={setSelectedCommandByName}
      >
        {props.commands.map((command) => {
          return (
            <Nav.Item key={command.type}>
              <Nav.Link eventKey={command.type}>{command.type}</Nav.Link>
            </Nav.Item>
          );
        })}
      </Nav>
    );
  }

  return (
    <div className={"command-display"}>
      {renderNav()}
      <Card>
        <div
          style={{ overflow: "auto", padding: "0.5em" }}
          onKeyDown={handleKeyDown}
          tabIndex={-1}
        >
          <CopyToClipboard
            text={selectedCommand.command}
            className="pull-right btn-sm"
          >
            <Button
              style={{ margin: "-0.5em" }}
              title="Copy to Clipboard"
              onClick={props.onCopy}
            >
              <FontAwesomeIcon icon={faClipboard} />
            </Button>
          </CopyToClipboard>
          <code style={{ whiteSpace: "pre-wrap" }}>
            {selectedCommand.command}
          </code>
        </div>
      </Card>
    </div>
  );
}

commandDisplay.propTypes = {
  commands: PropTypes.arrayOf(
    PropTypes.exact({
      type: PropTypes.string,
      command: PropTypes.string,
    }),
  ),
};
