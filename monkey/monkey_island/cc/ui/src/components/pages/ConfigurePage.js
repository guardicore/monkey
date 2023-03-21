import React from 'react';
import Form from '@rjsf/bootstrap-4';
import {Col, Nav} from 'react-bootstrap';
import _ from 'lodash';
import AuthComponent from '../AuthComponent';
import UiSchema from '../configuration-components/UiSchema';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck} from '@fortawesome/free-solid-svg-icons/faCheck';
import {faExclamationCircle} from '@fortawesome/free-solid-svg-icons/faExclamationCircle';
import {formValidationFormats} from '../configuration-components/ValidationFormats';
import transformErrors from '../configuration-components/ValidationErrorMessages';
import PropagationConfig, {
  EXPLOITERS_CONFIG_PATH
} from '../configuration-components/PropagationConfig'
import UnsafeConfigOptionsConfirmationModal
  from '../configuration-components/UnsafeConfigOptionsConfirmationModal.js';
import isUnsafeOptionSelected from '../utils/SafeOptionValidator.js';
import ConfigExportModal from '../configuration-components/ExportConfigModal';
import ConfigImportModal from '../configuration-components/ImportConfigModal';
import applyUiSchemaManipulators from '../configuration-components/UISchemaManipulators.tsx';
import CONFIGURATION_TABS_PER_MODE from '../configuration-components/ConfigurationTabs.js';
import {SCHEMA} from '../../services/configuration/configSchema.js';
import {
  reformatConfig,
  formatCredentialsForForm,
  formatCredentialsForIsland, reformatSchema
} from '../configuration-components/ReformatHook';
import {customizeValidator} from '@rjsf/validator-ajv8';
import LoadingIcon from '../ui-components/LoadingIcon';
import mergeAllOf from 'json-schema-merge-allof';
import RefParser from '@apidevtools/json-schema-ref-parser';
import CREDENTIALS from '../../services/configuration/propagation/credentials';

const CONFIG_URL = '/api/agent-configuration';
const SCHEMA_URL = '/api/agent-configuration-schema';
const RESET_URL = '/api/reset-agent-configuration';
const CONFIGURED_PROPAGATION_CREDENTIALS_URL = '/api/propagation-credentials/configured-credentials';
const configSubmitAction = 'config-submit';
const configExportAction = 'config-export';
const configSaveAction = 'config-saved';

class ConfigurePageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.currentSection = this.getSectionsOrder()[0];
    this.validator = customizeValidator( {customFormats: formValidationFormats});

    this.state = {
      configuration: {},
      credentials: {},
      currentFormData: {},
      importCandidateConfig: null,
      lastAction: 'none',
      schema: null,
      sections: [],
      selectedSection: this.currentSection,
      showUnsafeOptionsConfirmation: false,
      showConfigExportModal: false,
      showConfigImportModal: false,
      selectedExploiters: new Set()
    };
  }

  componentDidUpdate() {
    if (!this.getSectionsOrder().includes(this.currentSection)) {
      this.currentSection = this.getSectionsOrder()[0]
      this.setState({selectedSection: this.currentSection})
    }
  }

  resetLastAction = () => {
    this.setState({lastAction: 'none'});
  }

  getSectionsOrder() {
    let islandModeSet = (this.props.islandMode !== 'unset' && this.props.islandMode !== undefined)
    let islandMode = islandModeSet ? this.props.islandMode : 'advanced'
    return CONFIGURATION_TABS_PER_MODE[islandMode];
  }

  componentDidMount = () => {
    this.authFetch(SCHEMA_URL).then(res => res.json())
      .then((schema) => {
        RefParser.dereference(schema).then((schema) => {
          schema = mergeAllOf(schema);
          schema = reformatSchema(schema);
          this.setState({schema: schema});
    })});

    this.authFetch(CONFIG_URL).then(res => res.json())
      .then(monkeyConfig => {
        let sections = [];
        monkeyConfig = reformatConfig(monkeyConfig);

        for (let sectionKey of this.getSectionsOrder()) {
          sections.push({
            key: sectionKey,
            title: SCHEMA.properties[sectionKey].title
          });
        }
        this.setState({
          configuration: monkeyConfig,
          selectedExploiters: new Set(Object.keys(_.get(monkeyConfig, EXPLOITERS_CONFIG_PATH))),
          sections: sections,
          currentFormData: _.cloneDeep(monkeyConfig[this.state.selectedSection])
        })
      });
    this.updateCredentials();
  };

  onUnsafeConfirmationCancelClick = () => {
    this.setState({showUnsafeOptionsConfirmation: false, lastAction: 'none'});
  }

  onUnsafeConfirmationContinueClick = () => {
    this.setState({showUnsafeOptionsConfirmation: false});
    if (this.state.lastAction === configSubmitAction) {
      let config = this.filterUnselectedPlugins();
      this.configSubmit(config);
    } else if (this.state.lastAction === configExportAction) {
      let config = this.filterUnselectedPlugins();
      this.configSubmit(config);
      this.setState({showConfigExportModal: true});
    }
  }

  updateCredentials = () => {
    this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL)
      .then(res => res.json())
      .then(credentials => {
        credentials = formatCredentialsForForm(credentials);
        this.setState({
          credentials: credentials
        });
      });
  }

  updateConfig = () => {
    this.updateCredentials();
    this.authFetch(CONFIG_URL)
      .then(res => res.json())
      .then(data => {
        data = reformatConfig(data);
        this.setState({
          selectedExploiters: new Set(Object.keys(_.get(data, EXPLOITERS_CONFIG_PATH))),
          configuration: data,
          currentFormData: _.cloneDeep(data[this.state.selectedSection])
        });
      });
  }

  setSelectedExploiters = (exploiters) => {
    this.setState({selectedExploiters: exploiters})
  }

  onSubmit = () => {
    this.setState({lastAction: configSubmitAction}, this.attemptConfigSubmit)
  };

  canSafelySubmitConfig(config) {
    return !isUnsafeOptionSelected(this.state.schema, config);
  }

  async attemptConfigSubmit() {
    let config = this.filterUnselectedPlugins();
    if (this.canSafelySubmitConfig(config)) {
      this.configSubmit(config);
      if (this.state.lastAction === configExportAction) {
        this.setState({showConfigExportModal: true})
      }
    } else {
      this.setState({showUnsafeOptionsConfirmation: true});
    }
  }

  // rjsf component automatically creates an instance from the defaults in the schema
  // https://github.com/rjsf-team/react-jsonschema-form/issues/2980
  // Until the issue is fixed, we need to manually remove plugins that were not selected before
  // submitting/exporting the configuration
  filterUnselectedPlugins() {
    let filteredExploiters = {};
    let exploiterFormData = _.get(this.state.configuration, EXPLOITERS_CONFIG_PATH);
    for (let exploiter of [...this.state.selectedExploiters]) {
      if (exploiterFormData[exploiter] === undefined) {
        filteredExploiters[exploiter] = {};
      } else {
        filteredExploiters[exploiter] = exploiterFormData[exploiter];
      }
    }
    let config = _.cloneDeep(this.state.configuration)
    _.set(config, EXPLOITERS_CONFIG_PATH, filteredExploiters)
    return config;
  }

  configSubmit(config) {
    this.sendCredentials().then(res => {
      if (res.ok) {
        this.sendConfig(config);
      }
    });
  }

  onChange = (formData) => {
    let configuration = this.state.configuration;
    configuration[this.state.selectedSection] = formData;
    this.setState({currentFormData: formData, configuration: configuration});
  };

  onCredentialChange = (credentials) => {
    this.setState({credentials: credentials});
  }

  renderConfigExportModal = () => {
    return (<ConfigExportModal show={this.state.showConfigExportModal}
                               configuration={this.filterUnselectedPlugins()}
                               credentials={this.state.credentials}
                               onHide={() => {
                                 this.setState({showConfigExportModal: false});
                               }}/>);
  }

  renderConfigImportModal = () => {
    return (<ConfigImportModal show={this.state.showConfigImportModal}
                               schema={this.state.schema}
                               onClose={this.onClose}/>);
  }

  onClose = (importSuccessful) => {
    if (importSuccessful === true) {
      this.updateConfig();
      this.setState({
        lastAction: 'import_success',
        showConfigImportModal: false
      });

    } else {
      this.setState({showConfigImportModal: false});
    }
  }

  renderUnsafeOptionsConfirmationModal() {
    return (
      <UnsafeConfigOptionsConfirmationModal
        show={this.state.showUnsafeOptionsConfirmation}
        onCancelClick={this.onUnsafeConfirmationCancelClick}
        onContinueClick={this.onUnsafeConfirmationContinueClick}
      />
    );
  }

  setSelectedSection = (key) => {
    this.resetLastAction();
    this.currentSection = key;
    let selectedSectionData = this.state.configuration[key];

    this.setState({
      selectedSection: key,
      currentFormData: selectedSectionData
    });
  };

  resetConfig = () => {
    this.authFetch(RESET_URL,
      {
        method: 'POST'
      })
      .then(res => res.json())
      .then(() => {
          this.setState({
            lastAction: 'reset'
          });
          this.updateConfig();
          this.props.onStatusChange();
        }
      )
      .then(this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL, {method: 'PUT', body: '[]'}));
  };

  exportConfig = async () => {
    await this.setState({lastAction: configExportAction});
    await this.attemptConfigSubmit();
  };

  sendConfig(config) {
    config = reformatConfig(config, true);

    return (
      this.authFetch(CONFIG_URL,
        {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(config)
        })
        .then(res => {
          if (!res.ok) {
            console.log(`bad configuration submited ${res.status}`);
            this.setState({lastAction: 'invalid_configuration'});
          } else {
            this.setState({
              lastAction: configSaveAction
            });
            this.props.onStatusChange();
          }
          return res;
        }));
  }

  sendCredentials() {
    return (
      this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL,
        {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(formatCredentialsForIsland(this.state.credentials))
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

  renderConfigContent = (displayedSchema) => {
    let formProperties = {};
    let fullUiSchema = UiSchema({
      selectedSection: this.state.selectedSection
    })
    formProperties['schema'] = displayedSchema
    formProperties['onChange'] = this.onChange;
    formProperties['onFocus'] = this.resetLastAction;
    formProperties['transformErrors'] = transformErrors;
    formProperties['className'] = 'config-form';
    formProperties['liveValidate'] = true;
    formProperties['formData'] = this.state.currentFormData;
    formProperties['validator'] = this.validator;

    applyUiSchemaManipulators(this.state.selectedSection,
      formProperties['formData'],
      fullUiSchema);

    if (this.state.selectedSection === 'propagation') {
      delete Object.assign(formProperties, {'configuration': formProperties.formData}).formData;
      return (<PropagationConfig {...formProperties}
                                 fullUiSchema={fullUiSchema}
                                 credentials={this.state.credentials}
                                 selectedExploiters={this.state.selectedExploiters}
                                 setSelectedExploiters={this.setSelectedExploiters}
                                 onCredentialChange={this.onCredentialChange}/>)
    } else {
      formProperties['onChange'] = (formData) => {
        this.onChange(formData.formData)
      };
      return (
        <div>
          <Form {...formProperties} uiSchema={fullUiSchema} key={displayedSchema.title}>
            <button type='submit' className={'hidden'}>Submit</button>
          </Form>
        </div>
      )
    }
  };

  renderNav = () => {
    return (<Nav variant='tabs'
                 fill
                 activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
                 style={{'marginBottom': '2em'}}
                 className={'config-nav'}>
      {this.state.sections.map(section => {
        return (
          <Nav.Item key={section.key}>
            <Nav.Link eventKey={section.key}>{section.title}</Nav.Link>
          </Nav.Item>);
      })}
    </Nav>)
  };

  isSubmitDisabled = () => {
    if(_.isEmpty(this.state.configuration)){
      return true;
    }
    let errors = this.validator.validateFormData(this.state.configuration, this.state.schema);
    let credentialErrors = this.validator.validateFormData(this.state.credentials, CREDENTIALS);
    return errors.errors.length+credentialErrors.errors.length > 0
  }

  render() {
    if (this.state.schema === null) {
      return (<Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 8}} xl={{offset: 2, span: 8}}
                   className={'main'}><LoadingIcon /></Col>)
    }

    let displayedSchema = {};
    if (Object.prototype.hasOwnProperty.call(this.state.schema, 'properties')) {
      displayedSchema = this.state.schema['properties'][this.state.selectedSection];
      displayedSchema['definitions'] = this.state.schema['definitions'];
    }

    let content = '';
    if (Object.entries(this.state.configuration).length !== 0) {
      content = this.renderConfigContent(displayedSchema)
    }

    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 8}} xl={{offset: 2, span: 8}}
           className={'main'}>
        {this.renderConfigExportModal()}
        {this.renderConfigImportModal()}
        {this.renderUnsafeOptionsConfirmationModal()}
        <h1 className='page-title'>Monkey Configuration</h1>
        {this.renderNav()}
        {content}
        <div className='text-center'>
          <button type='submit' onClick={this.onSubmit} className='btn btn-success btn-lg'
                  style={{margin: '5px'}}
          disabled={this.isSubmitDisabled()}>
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
          {this.state.lastAction === configSaveAction ?
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
