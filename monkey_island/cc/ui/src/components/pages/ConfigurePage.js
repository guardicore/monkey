import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';
import fileDownload from 'js-file-download';

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
      lastAction: 'none',
      sections: [],
      selectedSection: 'basic',
      allMonkeysAreDead: true
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
    this.updateMonkeysRunning();
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
          lastAction: 'saved',
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
          lastAction: 'reset',
          schema: res.schema,
          configuration: res.configuration
        });
        this.props.onStatusChange();
      });
  };

  onReadFile = (event) => {
    try {
      this.setState({
        configuration: JSON.parse(event.target.result),
        selectedSection: 'basic',
        lastAction: 'import_success'
      });
      this.currentSection = 'basic';
      this.currentFormData = {};
    } catch(SyntaxError) {
      this.setState({lastAction: 'import_failure'});
    }
  };

  exportConfig = () => {
    this.updateConfigSection();
    fileDownload(JSON.stringify(this.state.configuration, null, 2), 'monkey.conf');
  };

  importConfig = (event) => {
    let reader = new FileReader();
    reader.onload = this.onReadFile;
    reader.readAsText(event.target.files[0]);
    event.target.value = null;
  };

  updateMonkeysRunning = () => {
    fetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        this.setState({
          allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done'])
        });
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
              The Monkey scans its subnet if "Local network scan" is ticked. Additionally the monkey scans machines
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
              { this.state.allMonkeysAreDead ?
                '' :
                <div className="alert alert-warning">
                  <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
                  Some monkeys are currently running. Note that changing the configuration will only apply to new
                  infections.
                </div>
              }
              <div className="text-center">
                <button type="submit" className="btn btn-success btn-lg" style={{margin: '5px'}}>
                  Submit
                </button>
                <button type="button" onClick={this.resetConfig} className="btn btn-danger btn-lg" style={{margin: '5px'}}>
                  Reset to defaults
                </button>
              </div>
            </div>
          </Form>
          : ''}
        <div className="text-center">
          <button onClick={() => document.getElementById('uploadInputInternal').click()}
                  className="btn btn-info btn-lg" style={{margin: '5px'}}>
            Import Config
          </button>
          <input id="uploadInputInternal" type="file" accept=".conf" onChange={this.importConfig} style={{display: 'none'}} />
          <button type="button" onClick={this.exportConfig} className="btn btn-info btn-lg" style={{margin: '5px'}}>
            Export config
          </button>
        </div>
        <div>
          { this.state.lastAction === 'reset' ?
            <div className="alert alert-success">
              <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
              Configuration reset successfully.
            </div>
            : ''}
          { this.state.lastAction === 'saved' ?
            <div className="alert alert-success">
              <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
              Configuration saved successfully.
            </div>
            : ''}
          { this.state.lastAction === 'import_failure' ?
            <div className="alert alert-danger">
              <i className="glyphicon glyphicon-exclamation-sign" style={{'marginRight': '5px'}}/>
              Failed importing configuration. Invalid config file.
            </div>
            : ''}
          { this.state.lastAction === 'import_success' ?
            <div className="alert alert-success">
              <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
              Configuration imported successfully.
            </div>
            : ''}
        </div>

      </Col>
    );
  }
}

export default ConfigurePageComponent;
