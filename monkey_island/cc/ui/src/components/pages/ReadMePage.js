import React from 'react';
import {Col, Nav, NavItem} from 'react-bootstrap';
var marked = require('marked');

var aboutDoc = require('raw!../../readme/About.md');
var usageDoc = require('raw!../../readme/Usage.md');
var howItWorksDoc = require('raw!../../readme/HowItWorks.md');
var licenseDoc = require('raw!../../readme/License.md');

class ReadMePageComponent extends React.Component {
  constructor(props) {
    super(props);

    this.sectionKeys = ['about', 'howItWorks', 'usage', 'license'];
    this.sections =
      {
        about: {title: 'About', data: aboutDoc},
        usage: {title: 'Usage', data: usageDoc},
        howItWorks: {title: 'How It Works', data: howItWorksDoc},
        license: {title: 'License', data: licenseDoc}
      };

    this.state = {
      selectedSection: this.sectionKeys[0]
    }
  }

  setSelectedSection = (key) => {
    this.setState({
      selectedSection: key
    });
  };

  render() {

    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">Read Me</h1>
        <Nav bsStyle="tabs" justified
             activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
             style={{'marginBottom': '2em'}}>
          {this.sectionKeys.map(section =>
            <NavItem key={section} eventKey={section}>{this.sections[section].title}</NavItem>
          )}
        </Nav>
        <div dangerouslySetInnerHTML={{__html: marked(this.sections[this.state.selectedSection].data)}} className="markdown-body">
        </div>
      </Col>
    );
  }
}

export default ReadMePageComponent;
