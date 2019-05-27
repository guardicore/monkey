import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';
import fileDownload from 'js-file-download';
import AuthComponent from '../AuthComponent';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

class ConfigurePageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.PBAwindowsPond = null;
    this.PBAlinuxPond = null;
    this.currentSection = 'basic';
    this.currentFormData = {};
    this.sectionsOrder = ['basic', 'basic_network', 'monkey', 'cnc', 'network', 'exploits', 'internal'];
    this.uiSchema = {
      behaviour: {
        custom_PBA_linux_cmd: {
          "ui:widget": "textarea",
          "ui:emptyValue": ""
        },
        PBA_linux_file: {
          "ui:widget": this.PBAlinux
        },
        custom_PBA_windows_cmd: {
          "ui:widget": "textarea",
          "ui:emptyValue": ""
        },
        PBA_windows_file: {
          "ui:widget": this.PBAwindows
        },
        PBA_linux_filename: {
          classNames: "linux-pba-file-info",
          "ui:emptyValue": ""
        },
        PBA_windows_filename: {
          classNames: "windows-pba-file-info",
          "ui:emptyValue": ""
        }
      }
    };
    // set schema from server
    this.state = {
      schema: {},
      configuration: {},
      lastAction: 'none',
      sections: [],
      selectedSection: 'basic',
      allMonkeysAreDead: true,
      PBAwinFile: [],
      PBAlinuxFile: []
    };
  }

  componentDidMount() {
    this.authFetch('/api/configuration/island')
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
    this.sendConfig()
      .then(res => res.json())
      .then(res => {
        this.setState({
          lastAction: 'saved',
          schema: res.schema,
          configuration: res.configuration
        });
        this.props.onStatusChange();
      }).catch(error => {
        console.log('bad configuration');
        this.setState({lastAction: 'invalid_configuration'});
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
    this.removePBAfiles();
    this.authFetch('/api/configuration/island',
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

  removePBAfiles(){
    // We need to clean files from widget, local state and configuration (to sync with bac end)
    if (this.PBAwindowsPond !== null){
      this.PBAwindowsPond.removeFile();
    }
    if (this.PBAlinuxPond !== null){
      this.PBAlinuxPond.removeFile();
    }
    let request_options = {method: 'DELETE',
                           headers: {'Content-Type': 'text/plain'}};
    this.authFetch('/api/fileUpload/PBAlinux', request_options);
    this.authFetch('/api/fileUpload/PBAwindows', request_options);
    this.setState({PBAlinuxFile: [], PBAwinFile: []});
  }

  onReadFile = (event) => {
    try {
      this.setState({
        configuration: JSON.parse(event.target.result),
        selectedSection: 'basic',
        lastAction: 'import_success'
      }, () => {this.sendConfig()});
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

  sendConfig() {
    return (
      this.authFetch('/api/configuration/island',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(this.state.configuration)
      })
      .then(res => {
        if (!res.ok)
        {
          throw Error()
        }
        return res;
      }).catch(error => {
        console.log('bad configuration');
        this.setState({lastAction: 'invalid_configuration'});
      }));
  };

  importConfig = (event) => {
    let reader = new FileReader();
    reader.onload = this.onReadFile;
    reader.readAsText(event.target.files[0]);
    event.target.value = null;
  };

  updateMonkeysRunning = () => {
    this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        // This check is used to prevent unnecessary re-rendering
        let allMonkeysAreDead = (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done']);
        if (allMonkeysAreDead !== this.state.allMonkeysAreDead) {
          this.setState({
            allMonkeysAreDead: allMonkeysAreDead
          });
        }
      });
  };

  PBAwindows = () => {
    return (<FilePond
      server={{ url:'/api/fileUpload/PBAwindows',
                process: {headers: {'Authorization': this.jwtHeader}},
                revert: {headers: {'Authorization': this.jwtHeader}},
                restore: {headers: {'Authorization': this.jwtHeader}},
                load: {headers: {'Authorization': this.jwtHeader}},
                fetch: {headers: {'Authorization': this.jwtHeader}}
      }}
      files={this.getWinPBAfile()}
      onupdatefiles={fileItems => {
        this.setState({
          PBAwinFile: fileItems.map(fileItem => fileItem.file)
        })
      }}
      ref={ref => this.PBAwindowsPond = ref}
    />)
  };

  PBAlinux = () => {
    return (<FilePond
      server={{ url:'/api/fileUpload/PBAlinux',
                process: {headers: {'Authorization': this.jwtHeader}},
                revert: {headers: {'Authorization': this.jwtHeader}},
                restore: {headers: {'Authorization': this.jwtHeader}},
                load: {headers: {'Authorization': this.jwtHeader}},
                fetch: {headers: {'Authorization': this.jwtHeader}}
      }}
      files={this.getLinuxPBAfile()}
      onupdatefiles={fileItems => {
        this.setState({
          PBAlinuxFile: fileItems.map(fileItem => fileItem.file)
        })
      }}
      ref={ref => this.PBAlinuxPond = ref}
    />)
  };

  getWinPBAfile(){
    if (this.state.PBAwinFile.length !== 0){
      return ConfigurePageComponent.getMockPBAfile(this.state.PBAwinFile[0])
    } else if (this.state.configuration.monkey.behaviour.PBA_windows_filename){
      return ConfigurePageComponent.getFullPBAfile(this.state.configuration.monkey.behaviour.PBA_windows_filename)
    }
  }

  getLinuxPBAfile(){
    if (this.state.PBAlinuxFile.length !== 0){
      return ConfigurePageComponent.getMockPBAfile(this.state.PBAlinuxFile[0])
    } else if (this.state.configuration.monkey.behaviour.PBA_linux_filename) {
      return ConfigurePageComponent.getFullPBAfile(this.state.configuration.monkey.behaviour.PBA_linux_filename)
    }
  }

  static getFullPBAfile(filename){
    return [{
      source: filename,
      options: {
        type: 'limbo'
      }
    }];
  }

  static getMockPBAfile(mockFile){
    let pbaFile = [{
      source: mockFile.name,
      options: {
        type: 'limbo'
      }
    }];
    pbaFile[0].options.file = mockFile;
    return pbaFile
  }

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
                uiSchema={this.uiSchema}
                formData={this.state.configuration[this.state.selectedSection]}
                onSubmit={this.onSubmit}
                onChange={this.onChange}
                noValidate={true}>
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
          { this.state.lastAction === 'invalid_configuration' ?
            <div className="alert alert-danger">
              <i className="glyphicon glyphicon-exclamation-sign" style={{'marginRight': '5px'}}/>
              An invalid configuration file was imported or submitted.
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
