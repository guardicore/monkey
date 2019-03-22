import React from 'react';
import AuthComponent from '../AuthComponent';
import 'filepond/dist/filepond.min.css';
import MatrixComponent from '../attack/MatrixComponent'

class AttckComponent extends AuthComponent {
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
    content = (<MatrixComponent configuration={this.state.configuration} />);
    return <div>{content}</div>;
  }
}

export default AttckComponent;
