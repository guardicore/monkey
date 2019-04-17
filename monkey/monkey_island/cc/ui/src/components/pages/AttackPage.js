import React from 'react';
import AuthComponent from '../AuthComponent';
import 'filepond/dist/filepond.min.css';
import MatrixComponent from '../attack/MatrixComponent'
import {Col} from "react-bootstrap";
import '../../styles/Checkbox.scss'

class AttackComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.currentSection = 'ATT&CK matrix';
    this.currentFormData = {};
    this.sectionsOrder = ['ATT&CK matrix'];
    // set schema from server
    this.state = {
      configuration: {},
      sections: [],
      selectedSection: 'ATT&CK matrix',
    };
  }

  componentDidMount() {
    this.authFetch('/api/attack')
      .then(res => res.json())
      .then(res => {
        let sections = [];
        for (let sectionKey of this.sectionsOrder) {
          sections.push({key: sectionKey, title: res.configuration.title});
        }
        this.setState({
          configuration: res.configuration,
          sections: sections,
          selectedSection: 'ATT&CK matrix'
        });
      });
  }

  render() {
    let content;
    if (Object.keys(this.state.configuration).length === 0) {
      content = (<h1>Fetching configuration...</h1>);
    } else {
      content = (
        <div>
          <div id="header" className="row justify-content-between attack-legend">
            <Col xs={4}>
              <i className="fa fa-circle-thin icon-unchecked"></i>
              <span> - Dissabled</span>
            </Col>
            <Col xs={4}>
              <i className="fa fa-circle icon-checked"></i>
              <span> - Enabled</span>
            </Col>
            <Col xs={4}>
              <i className="fa fa-circle icon-mandatory"></i>
              <span> - Mandatory</span>
            </Col>
          </div>
          <MatrixComponent configuration={this.state.configuration} />
        </div>);
    }
    return <div>{content}</div>;
  }
}

export default AttackComponent;
