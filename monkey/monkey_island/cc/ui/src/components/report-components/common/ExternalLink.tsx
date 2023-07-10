import React, { ReactFragment, ReactElement } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExternalLinkSquareAlt } from "@fortawesome/free-solid-svg-icons";

type Props = {
  url: string;
  text: string;
};

function ExternalLink(props: Props): ReactElement {
  return (
    <a href={props.url} target="_blank" rel="noreferrer">
      {props.text}
      <FontAwesomeIcon
        icon={faExternalLinkSquareAlt}
        className="external-link-icon"
      />
    </a>
  );
}

export default ExternalLink;
