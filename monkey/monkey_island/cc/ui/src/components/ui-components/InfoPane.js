import {Card, Button} from 'react-bootstrap';
import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faQuestionCircle} from '@fortawesome/free-solid-svg-icons';

import {getObjectFromRegistryByRef} from './JsonSchemaHelpers';

function getDefaultPaneParams(refString, registry) {
  let configSection = getObjectFromRegistryByRef(refString, registry);
  return ({title: configSection.title, content: configSection.description});
}

function InfoPane(props) {
  return (
    <Card className={'info-pane'}>
      {getTitle(props)}
      {getSubtitle(props)}
      {getBody(props)}
    </Card>);
}

function getTitle(props) {
  if (typeof (props.title) == 'string') {
    return (
      <Card.Title className={'pane-title'}>
        {props.title}
        {getLinkButton(props)}
      </Card.Title>)
  }
}

function getLinkButton(props) {
  if (typeof (props.link) == 'string') {
    return (
      <Button variant={'link'} className={'pane-link'} href={props.link} target={'_blank'}>
        <FontAwesomeIcon icon={faQuestionCircle}/>
      </Button>)
  }
}

function getSubtitle(props) {
  if (typeof (props.subtitle) == 'string') {
    return (
      <Card.Subtitle className={'pane-subtitle'}>
        {props.subtitle}
      </Card.Subtitle>)
  }
}

function getBody(props) {
  return (
    <Card.Body className={'pane-body'}>
      {props.body}
    </Card.Body>
  )
}

export {getDefaultPaneParams, InfoPane}
