import React from 'react';
import {Col} from 'react-bootstrap';
var marked = require('marked');

var markdown = require('raw!../../README.md');

class ReadMePageComponent extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {

    return (
      <Col xs={8}>
        <h1 className="page-title">Read Me</h1>
        <div dangerouslySetInnerHTML={{__html: marked(markdown)}} className="markdown-body">
        </div>
      </Col>
    );
  }
}

export default ReadMePageComponent;
