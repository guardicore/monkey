import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';

class ConfigurePageComponent extends React.Component {
  constructor(props) {
    super(props);

    this.currentSection = 'basic';
    this.currentFormData = {};
    this.sectionsOrder = ['basic', 'basic_network', 'monkey', 'cnc', 'network', 'exploits', 'internal'];

    // set schema from server
    this.state = {
      schema: {},
      configuration: {},
      saved: false,
      reset: false,
      sections: [],
      selectedSection: 'basic'
    };
  }

  componentDidMount() {
    fetch('/api/configuration')
      .then(res => res.json())
      .then(res => {
        let sections = [];
        for (let sectionKey of this.sectionsOrder) {
          sections.push({key: sectionKey, title: res.schema.properties[sectionKey].title});
        }
        this.setState({
          schema: res.schema,
          configuration: res.configuration,
          sections: sections,
          selectedSection: 'basic'
        })
      });
  }

  onSubmit = ({formData}) => {
    this.currentFormData = formData;
    this.updateConfigSection();
    fetch('/api/configuration',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(this.state.configuration)
      })
      .then(res => res.json())
      .then(res => {
        this.setState({
          saved: true,
          reset: false,
          schema: res.schema,
          configuration: res.configuration
        });
        this.props.onStatusChange();
      });
  };

  onChange = ({formData}) => {
    this.currentFormData = formData;
  };

  updateConfigSection = () => {
    let newConfig = this.state.configuration;
    if (Object.keys(this.currentFormData).length > 0) {
      newConfig[this.currentSection] = this.currentFormData;
      this.currentFormData = {};
    }
    this.setState({configuration: newConfig});
  };

  setSelectedSection = (key) => {
    this.updateConfigSection();
    this.currentSection = key;
    this.setState({
      selectedSection: key
    });
  };

  resetConfig = () => {
    fetch('/api/configuration',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'reset': true})
      })
      .then(res => res.json())
      .then(res => {
        this.setState({
          reset: true,
          saved: false,
          schema: res.schema,
          configuration: res.configuration
        });
        this.props.onStatusChange();
      });
  };

  render() {
    let displayedSchema = {};
    if (this.state.schema.hasOwnProperty('properties')) {
      displayedSchema = this.state.schema['properties'][this.state.selectedSection];
      displayedSchema['definitions'] = this.state.schema['definitions'];
    }

    return (
      <Col xs={12} lg={8}>
        <h1 className="page-title">Monkey Configuration</h1>
        <Nav bsStyle="tabs" justified
             activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
             style={{'marginBottom': '2em'}}>
          {this.state.sections.map(section =>
            <NavItem key={section.key} eventKey={section.key}>{section.title}</NavItem>
          )}
        </Nav>
        {
          this.state.selectedSection === 'basic_network' ?
            <div className="alert alert-info">
              <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
              The Monkey scans its subnet if "Local network scan" is ticked. Additionally the monkey will scan machines
              according to its range class.
            </div>
            : <div />
        }
        { this.state.selectedSection ?
          <Form schema={displayedSchema}
                formData={this.state.configuration[this.state.selectedSection]}
                onSubmit={this.onSubmit}
                onChange={this.onChange}>
            <div>
              <div className="alert alert-info">
                <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
                Changing the configuration will only apply to new infections.
              </div>
              <div className="alert alert-warning">
                <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
                Changing config values with the &#9888; mark may result in the monkey propagating too far or using dangerous exploits.
              </div>
              <div className="text-center">
                <button type="submit" className="btn btn-success btn-lg" style={{margin: '5px'}}>
                  Submit
                </button>
                <button type="button" onClick={this.resetConfig} className="btn btn-danger btn-lg" style={{margin: '5px'}}>
                  Reset to defaults
                </button>
              </div>
              { this.state.reset ?
                <div className="alert alert-success">
                  <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
                  Configuration reset successfully.
                </div>
                : ''}
              { this.state.saved ?
                <div className="alert alert-success">
                  <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
                  Configuration saved successfully.
                </div>
                : ''}
            </div>
          </Form>
          : ''}


      </Col>
    );
  }
}

export default ConfigurePageComponent;
