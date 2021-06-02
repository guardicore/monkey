import React from 'react';
import Form from 'react-jsonschema-form-bs4';
import {Button, Col, Modal, Nav} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ConfigMatrixComponent from '../attack/ConfigMatrixComponent';
import UiSchema from '../configuration-components/UiSchema';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faExclamationCircle} from '@fortawesome/free-solid-svg-icons/faExclamationCircle';
import {formValidationFormats} from '../configuration-components/ValidationFormats';
import transformErrors from '../configuration-components/ValidationErrorMessages';
import InternalConfig from '../configuration-components/InternalConfig';
import UnsafeOptionsConfirmationModal
  from '../configuration-components/UnsafeOptionsConfirmationModal.js';
import UnsafeOptionsWarningModal from '../configuration-components/UnsafeOptionsWarningModal.js';
import isUnsafeOptionSelected from '../utils/SafeOptionValidator.js';
import ConfigExportModal from '../configuration-components/ExportConfigModal';
import ConfigImportModal from '../configuration-components/ImportConfigModal';

const ATTACK_URL = '/api/attack';
const CONFIG_URL = '/api/configuration/island';
export const API_PBA_LINUX = '/api/fileUpload/PBAlinux';
export const API_PBA_WINDOWS = '/api/fileUpload/PBAwindows';

class ConfigurePageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.currentSection = 'attack';
    this.currentFormData = {};
    this.initialConfig = {};
    this.initialAttackConfig = {};
    this.sectionsOrder = ['attack', 'basic', 'basic_network', 'monkey', 'internal'];

    this.state = {
      attackConfig: {},
      configuration: {},
      importCandidateConfig: null,
      lastAction: 'none',
      schema: {},
      sections: [],
      selectedSection: 'attack',
      showAttackAlert: false,
      showUnsafeOptionsConfirmation: false,
      showUnsafeAttackOptionsWarning: false,
      showConfigExportModal: false,
      showConfigImportModal: false
    };
  }

  setInitialConfig(config) {
    // Sets a reference to know if config was changed
    this.initialConfig = JSON.parse(JSON.stringify(config));
  }

  setInitialAttackConfig(attackConfig) {
    // Sets a reference to know if attack config was changed
    this.initialAttackConfig = JSON.parse(JSON.stringify(attackConfig));
  }

  componentDidMount = () => {
    let urls = [CONFIG_URL, ATTACK_URL];
    Promise.all(urls.map(url => this.authFetch(url).then(res => res.json())))
      .then(data => {
        let sections = [];
        let attackConfig = data[1];
        let monkeyConfig = data[0];
        this.setInitialConfig(monkeyConfig.configuration);
        this.setInitialAttackConfig(attackConfig.configuration);
        for (let sectionKey of this.sectionsOrder) {
          if (sectionKey === 'attack') {
            sections.push({key: sectionKey, title: 'ATT&CK'})
          } else {
            sections.push({
              key: sectionKey,
              title: monkeyConfig.schema.properties[sectionKey].title
            });
          }
        }
        this.setState({
          schema: monkeyConfig.schema,
          configuration: monkeyConfig.configuration,
          attackConfig: attackConfig.configuration,
          sections: sections,
          selectedSection: 'attack'
        })
      });
  };

  onUnsafeConfirmationCancelClick = () => {
    this.setState({showUnsafeOptionsConfirmation: false});
  }

  onUnsafeConfirmationContinueClick = () => {
    this.setState({showUnsafeOptionsConfirmation: false});

    if (this.state.lastAction === 'submit_attempt') {
      this.configSubmit();
    }
  }

  onUnsafeAttackContinueClick = () => {
    this.setState({showUnsafeAttackOptionsWarning: false});
  }


  updateConfig = (callback = null) => {
    this.authFetch(CONFIG_URL)
      .then(res => res.json())
      .then(data => {
        this.setInitialConfig(data.configuration);
        this.setState({configuration: data.configuration}, callback);
      })
  };

  onSubmit = () => {
    if (this.state.selectedSection === 'attack') {
      this.matrixSubmit();
    } else {
      this.attemptConfigSubmit();
    }
  };

  // TODO add a safety check to config import
  canSafelySubmitConfig(config) {
    return !isUnsafeOptionSelected(this.state.schema, config);
  }

  matrixSubmit = () => {
    // Submit attack matrix
    this.authFetch(ATTACK_URL,
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(this.state.attackConfig)
      })
      .then(res => {
        if (!res.ok) {
          throw Error()
        }
        return res;
      })
      .then(() => {
        this.setInitialAttackConfig(this.state.attackConfig);
      })
      .then(() => this.updateConfig(this.checkAndShowUnsafeAttackWarning))
      .then(() => this.setState({lastAction: 'saved'}))
      .catch(error => {
        console.log('Bad configuration: ' + error.toString());
        this.setState({lastAction: 'invalid_configuration'});
      });
  };

  checkAndShowUnsafeAttackWarning = () => {
    if (isUnsafeOptionSelected(this.state.schema, this.state.configuration)) {
      this.setState({showUnsafeAttackOptionsWarning: true});
    }
  }

  attemptConfigSubmit() {
    this.updateConfigSection();
    this.setState({lastAction: 'submit_attempt'}, () => {
        if (this.canSafelySubmitConfig(this.state.configuration)) {
          this.configSubmit();
        } else {
          this.setState({showUnsafeOptionsConfirmation: true});
        }
      }
    );
  }

  configSubmit() {
    this.sendConfig()
      .then(res => res.json())
      .then(res => {
        this.setState({
          lastAction: 'saved',
          schema: res.schema,
          configuration: res.configuration
        });
        this.setInitialConfig(res.configuration);
        this.props.onStatusChange();
      }).catch(error => {
      console.log('Bad configuration: ' + error.toString());
      this.setState({lastAction: 'invalid_configuration'});
    });
  }

  // Alters attack configuration when user toggles technique
  attackTechniqueChange = (technique, value, mapped = false) => {
    // Change value in attack configuration
    // Go trough each column in matrix, searching for technique
    Object.entries(this.state.attackConfig).forEach(techType => {
      if (Object.prototype.hasOwnProperty.call(techType[1].properties, technique)) {
        let tempMatrix = this.state.attackConfig;
        tempMatrix[techType[0]].properties[technique].value = value;
        this.setState({attackConfig: tempMatrix});

        // Toggle all mapped techniques
        if (!mapped) {
          // Loop trough each column and each row
          Object.entries(this.state.attackConfig).forEach(otherType => {
            Object.entries(otherType[1].properties).forEach(otherTech => {
              // If this technique depends on a technique that was changed
              if (Object.prototype.hasOwnProperty.call(otherTech[1], 'depends_on') &&
                otherTech[1]['depends_on'].includes(technique)) {
                this.attackTechniqueChange(otherTech[0], value, true)
              }
            })
          });
        }
      }
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
    this.setState({configuration: newConfig, lastAction: 'none'});
  };

  renderConfigExportModal = () => {
    return (<ConfigExportModal show={this.state.showConfigExportModal}
                               onHide={() => {
                                 this.setState({showConfigExportModal: false});
                               }}/>);
  }

  renderConfigImportModal = () => {
    return (<ConfigImportModal show={this.state.showConfigImportModal}
                               onClose={this.onClose}/>);
  }

  onClose = (importSuccessful) => {
    if(importSuccessful === true){
      this.updateConfig();
      this.setState({lastAction: 'import_success',
                          showConfigImportModal: false});

    } else {
      this.setState({showConfigImportModal: false});
    }
  }

  renderAttackAlertModal = () => {
    return (<Modal show={this.state.showAttackAlert} onHide={() => {
      this.setState({showAttackAlert: false})
    }}>
      <Modal.Body>
        <h2>
          <div className='text-center'>Warning</div>
        </h2>
        <p className='text-center' style={{'fontSize': '1.2em', 'marginBottom': '2em'}}>
          You have unsubmitted changes. Submit them before proceeding.
        </p>
        <div className='text-center'>
          <Button type='button'
                  className='btn btn-success'
                  size='lg'
                  style={{margin: '5px'}}
                  onClick={() => {
                    this.setState({showAttackAlert: false})
                  }}>
            Cancel
          </Button>
        </div>
      </Modal.Body>
    </Modal>)
  };

  renderUnsafeOptionsConfirmationModal() {
    return (
      <UnsafeOptionsConfirmationModal
        show={this.state.showUnsafeOptionsConfirmation}
        onCancelClick={this.onUnsafeConfirmationCancelClick}
        onContinueClick={this.onUnsafeConfirmationContinueClick}
      />
    );
  }

  renderUnsafeAttackOptionsWarningModal() {
    return (
      <UnsafeOptionsWarningModal
        show={this.state.showUnsafeAttackOptionsWarning}
        onContinueClick={this.onUnsafeAttackContinueClick}
      />
    );
  }

  userChangedConfig() {
    if (JSON.stringify(this.state.configuration) === JSON.stringify(this.initialConfig)) {
      if (Object.keys(this.currentFormData).length === 0 ||
        JSON.stringify(this.initialConfig[this.currentSection]) === JSON.stringify(this.currentFormData)) {
        return false;
      }
    }
    return true;
  }

  userChangedMatrix() {
    return (JSON.stringify(this.state.attackConfig) !== JSON.stringify(this.initialAttackConfig))
  }

  setSelectedSection = (key) => {
    if ((key === 'attack' && this.userChangedConfig()) ||
      (this.currentSection === 'attack' && this.userChangedMatrix())) {
      this.setState({showAttackAlert: true});
      return;
    }
    this.updateConfigSection();
    this.currentSection = key;
    this.setState({
      selectedSection: key
    });
  };

  resetConfig = () => {
    this.authFetch(CONFIG_URL,
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
          this.setInitialConfig(res.configuration);
          this.props.onStatusChange();
        }
      ).then(() => {
      this.removePBAfile(API_PBA_WINDOWS, this.setPbaFilenameWindows)
      this.removePBAfile(API_PBA_LINUX, this.setPbaFilenameLinux)
    });
    this.authFetch(ATTACK_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify('reset_attack_matrix')
    })
      .then(res => res.json())
      .then(res => {
        this.setState({attackConfig: res.configuration});
        this.setInitialAttackConfig(res.configuration);
      })
  };

  removePBAfile(apiEndpoint, setFilenameFnc) {
    this.sendPbaRemoveRequest(apiEndpoint)
    setFilenameFnc('')
  }

  sendPbaRemoveRequest(apiEndpoint) {
    let request_options = {
      method: 'DELETE',
      headers: {'Content-Type': 'text/plain'}
    };
    this.authFetch(apiEndpoint, request_options);
  }

  exportConfig = () => {
    this.updateConfigSection();
    this.setState({showConfigExportModal: true});
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
          if (!res.ok) {
            throw Error()
          }
          return res;
        }).catch((error) => {
        console.log(`bad configuration ${error}`);
        this.setState({lastAction: 'invalid_configuration'});
      }));
  }

  renderMatrix = () => {
    return (<ConfigMatrixComponent configuration={this.state.attackConfig}
                                   submit={this.componentDidMount}
                                   reset={this.resetConfig}
                                   change={this.attackTechniqueChange}/>)
  };

  renderConfigContent = (displayedSchema) => {
    let formProperties = {};
    formProperties['schema'] = displayedSchema
    formProperties['uiSchema'] = UiSchema({
      PBA_linux_filename: this.state.configuration.monkey.post_breach.PBA_linux_filename,
      PBA_windows_filename: this.state.configuration.monkey.post_breach.PBA_windows_filename,
      setPbaFilenameWindows: this.setPbaFilenameWindows,
      setPbaFilenameLinux: this.setPbaFilenameLinux,
      selectedSection: this.state.selectedSection
    })
    formProperties['formData'] = this.state.configuration[this.state.selectedSection];
    formProperties['onChange'] = this.onChange;
    formProperties['customFormats'] = formValidationFormats;
    formProperties['transformErrors'] = transformErrors;
    formProperties['className'] = 'config-form';
    formProperties['liveValidate'] = true;

    if (this.state.selectedSection === 'internal') {
      return (<InternalConfig {...formProperties}/>)
    } else {
      return (
        <div>
          <Form {...formProperties}>
            <button type='submit' className={'hidden'}>Submit</button>
          </Form>
        </div>
      )
    }
  };

  setPbaFilenameWindows = (filename) => {
    let config = this.state.configuration
    config.monkey.post_breach.PBA_windows_filename = filename
    this.setState({
      configuration: config
    })
  }

  setPbaFilenameLinux = (filename) => {
    let config = this.state.configuration
    config.monkey.post_breach.PBA_linux_filename = filename
    this.setState({
      configuration: config
    })
  }

  renderNav = () => {
    return (<Nav variant='tabs'
                 fill
                 activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
                 style={{'marginBottom': '2em'}}
                 className={'config-nav'}>
      {this.state.sections.map(section => {
        let classProp = section.key.startsWith('basic') ? 'tab-primary' : '';
        return (
          <Nav.Item key={section.key}>
            <Nav.Link className={classProp} eventKey={section.key}>{section.title}</Nav.Link>
          </Nav.Item>);
      })}
    </Nav>)
  };

  render() {
    let displayedSchema = {};
    if (Object.prototype.hasOwnProperty.call(this.state.schema, 'properties') && this.state.selectedSection !== 'attack') {
      displayedSchema = this.state.schema['properties'][this.state.selectedSection];
      displayedSchema['definitions'] = this.state.schema['definitions'];
    }

    let content = '';
    if (this.state.selectedSection === 'attack' && Object.entries(this.state.attackConfig).length !== 0) {
      content = this.renderMatrix()
    } else if (this.state.selectedSection !== 'attack') {
      content = this.renderConfigContent(displayedSchema)
    }
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 8}} xl={{offset: 2, span: 8}}
           className={'main'}>
        {this.renderConfigExportModal()}
        {this.renderConfigImportModal()}
        {this.renderAttackAlertModal()}
        {this.renderUnsafeOptionsConfirmationModal()}
        {this.renderUnsafeAttackOptionsWarningModal()}
        <h1 className='page-title'>Monkey Configuration</h1>
        {this.renderNav()}
        {content}
        <div className='text-center'>
          <button type='submit' onClick={this.onSubmit} className='btn btn-success btn-lg'
                  style={{margin: '5px'}}>
            Submit
          </button>
          <button type='button' onClick={this.resetConfig} className='btn btn-danger btn-lg'
                  style={{margin: '5px'}}>
            Reset to defaults
          </button>
        </div>
        <div className='text-center'>
          <button onClick={() => {
            this.setState({showConfigImportModal: true})
          }}
                  className='btn btn-info btn-lg' style={{margin: '5px'}}>
            Import config
          </button>
          <button type='button'
                  onClick={this.exportConfig}
                  className='btn btn-info btn-lg' style={{margin: '5px'}}>
            Export config
          </button>
        </div>
        <div>
          {this.state.lastAction === 'reset' ?
            <div className='alert alert-success'>
              <FontAwesomeIcon icon={faCheck} style={{'marginRight': '5px'}}/>
              Configuration reset successfully.
            </div>
            : ''}
          {this.state.lastAction === 'saved' ?
            <div className='alert alert-success'>
              <FontAwesomeIcon icon={faCheck} style={{'marginRight': '5px'}}/>
              Configuration saved successfully.
            </div>
            : ''}
          {this.state.lastAction === 'invalid_configuration' ?
            <div className='alert alert-danger'>
              <FontAwesomeIcon icon={faExclamationCircle} style={{'marginRight': '5px'}}/>
              An invalid configuration file was imported or submitted.
            </div>
            : ''}
          {this.state.lastAction === 'import_success' ?
            <div className='alert alert-success'>
              <FontAwesomeIcon icon={faCheck} style={{'marginRight': '5px'}}/>
              Configuration imported successfully.
            </div>
            : ''}
        </div>
      </Col>
    );
  }
}

export default ConfigurePageComponent;
