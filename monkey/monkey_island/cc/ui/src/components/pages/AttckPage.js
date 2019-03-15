import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import 'filepond/dist/filepond.min.css';

class AttckComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.currentSection = 'ATT&CK matrix';
    this.currentFormData = {};
    this.sectionsOrder = ['ATT&CK matrix'];
    // set schema from server
    this.state = {
      schema: {},
      configuration: {},
      lastAction: 'none',
      sections: [],
      selectedSection: 'ATT&CK matrix',
    };
  }

  componentDidMount() {
    this.authFetch('/api/attck')
      .then(res => res.json())
      .then(res => {
        let sections = [];
        for (let sectionKey of this.sectionsOrder) {
          sections.push({key: sectionKey, title: res.configuration.title});
        }
        this.setState({
          schema: res.schema,
          configuration: res.configuration,
          sections: sections,
          selectedSection: 'ATT&CK matrix'
        })
      });
  }

  render() {
    return (<Col xs={12} lg={8}> Vakaris </Col>);
  }
}

export default AttckComponent;
