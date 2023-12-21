import React from 'react';
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
} from '../configuration-components/PropagationConfig';
import MasqueradeConfig from '../configuration-components/MasqueradeConfig';
import {CREDENTIALS_COLLECTORS_CONFIG_PATH, PAYLOADS_CONFIG_PATH} from '../configuration-components/PluginSelectorTemplate';
import {CONFIGURATION_TABS} from '../configuration-components/ConfigurationTabs.js'
import FormConfig from '../configuration-components/FormConfig';
import UnsafeConfigOptionsConfirmationModal
  from '../configuration-components/UnsafeConfigOptionsConfirmationModal.js';
import isUnsafeOptionSelected from '../utils/SafeOptionValidator.js';
import {
  getStringsFromBytes,
  getMasqueradesBytesArrays, getMasqueradeBytesSubsets, MASQUE_TYPES
} from '../utils/MasqueradeUtils.js';
import ConfigExportModal from '../configuration-components/ExportConfigModal';
import ConfigImportModal from '../configuration-components/ImportConfigModal';
import applyUiSchemaManipulators from '../configuration-components/UISchemaManipulators.tsx';
import CONFIGURATION_TABS_ORDER from '../configuration-components/ConfigurationTabs.js';
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
import {MASQUERADE} from '../../services/configuration/masquerade';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import {nanoid} from 'nanoid';
const CONFIG_URL = '/api/agent-configuration';
const SCHEMA_URL = '/api/agent-configuration-schema';
const RESET_URL = '/api/reset-agent-configuration';
const CONFIGURED_PROPAGATION_CREDENTIALS_URL = '/api/propagation-credentials/configured-credentials';
const configSubmitAction = 'config-submit';
const configExportAction = 'config-export';
const configSaveAction = 'config-saved';

const EMPTY_BYTES_ARRAY = new Uint8Array(new ArrayBuffer(0));

class ConfigurePageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.currentSection = CONFIGURATION_TABS_ORDER[0];
    this.validator = customizeValidator( {customFormats: formValidationFormats});

    this.state = {
      configuration: {},
      credentials: {credentialsData: [], errors: [], id: null},
      credentialsErrors: [],
      masqueStrings: {},
      currentFormData: {},
      importCandidateConfig: null,
      lastAction: 'none',
      schema: null,
      sections: [],
      selectedSection: this.currentSection,
      showUnsafeOptionsConfirmation: false,
      showConfigExportModal: false,
      showConfigImportModal: false,
      selectedPlugins: {}
    };
  }

  setCredentialsState = (rows = [], errors = [], isRequiredToUpdateId) => {
    let newState = {credentials: {credentialsData: rows, errors: errors, id: this.state.credentials.id}};
    if(isRequiredToUpdateId) {
      newState.credentials['id'] = nanoid();
    }
    this.setState(newState);
  }

  resetLastAction = () => {
    this.setState({lastAction: 'none'});
  }

  componentDidMount = () => {
    this.authFetch(SCHEMA_URL, {}, true).then(res => res.json())
      .then((schema) => {
        RefParser.dereference(schema).then((schema) => {
          schema = mergeAllOf(schema);
          schema = reformatSchema(schema);
          this.setState({schema: schema});
    })});

    this.authFetch(CONFIG_URL, {}, true).then(res => res.json())
      .then(monkeyConfig => {
        let sections = [];
        monkeyConfig = reformatConfig(monkeyConfig);

        for (let sectionKey of CONFIGURATION_TABS_ORDER) {
          sections.push({
            key: sectionKey,
            title: SCHEMA.properties[sectionKey].title
          });
        }
        this.setState({
          configuration: monkeyConfig,
          selectedPlugins: {
              [CONFIGURATION_TABS.PROPAGATION]: this.getSelectedPlugins(monkeyConfig, EXPLOITERS_CONFIG_PATH),
              [CONFIGURATION_TABS.CREDENTIALS_COLLECTORS]: this.getSelectedPlugins(monkeyConfig, CREDENTIALS_COLLECTORS_CONFIG_PATH),
              [CONFIGURATION_TABS.PAYLOADS]: this.getSelectedPlugins(monkeyConfig, PAYLOADS_CONFIG_PATH)
            },
          sections: sections,
          currentFormData: _.cloneDeep(monkeyConfig[this.state.selectedSection])
        })
      });
    this.updateCredentials();
    this.updateMasqueStrings();
  };

  getSelectedPlugins = (config, pluginTypeConfigPath) => {
    return new Set(Object.keys(_.get(config, pluginTypeConfigPath)))
  }

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
    this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL, {}, true)
      .then(res => res.json())
      .then(credentialsData => {
        const formattedCredentialsData = formatCredentialsForForm(credentialsData);
        this.setCredentialsState(formattedCredentialsData, [], true);
      });
  }

  updateMasqueStrings = async () => {
    const [linuxRes, windowsRes] = await Promise.all([
      IslandHttpClient.get(APIEndpoint.linuxMasque, {}, true),
      IslandHttpClient.get(APIEndpoint.windowsMasque, {}, true)
    ]);

    const linuxMasqueBytes = await linuxRes.body.arrayBuffer();
    const linuxMasquesSubsets = getMasqueradeBytesSubsets(linuxMasqueBytes);
    const linuxMasqueTexts = getStringsFromBytes(linuxMasqueBytes, MASQUE_TYPES.TEXTS, linuxMasquesSubsets[MASQUE_TYPES.TEXTS.key]);
    const linuxMasqueBase64 = getStringsFromBytes(linuxMasqueBytes, MASQUE_TYPES.BASE64, linuxMasquesSubsets[MASQUE_TYPES.BASE64.key]);

    const windowsMasqueBytes = await windowsRes.body.arrayBuffer();
    const windowsMasquesSubsets = getMasqueradeBytesSubsets(windowsMasqueBytes);
    const windowsMasqueTexts = getStringsFromBytes(windowsMasqueBytes, MASQUE_TYPES.TEXTS, windowsMasquesSubsets[MASQUE_TYPES.TEXTS.key]);
    const windowsMasqueBase64 = getStringsFromBytes(windowsMasqueBytes, MASQUE_TYPES.BASE64, windowsMasquesSubsets[MASQUE_TYPES.BASE64.key]);

    this.setState({
      masqueStrings: {
        linux: {
          masque_texts: linuxMasqueTexts,
          masque_base64: linuxMasqueBase64
        },
        windows: {
          masque_texts: windowsMasqueTexts,
          masque_base64: windowsMasqueBase64
        }
      }
    });
  }

  updateConfig = () => {
    this.updateCredentials();
    this.updateMasqueStrings();
    this.authFetch(CONFIG_URL, {}, true)
      .then(res => res.json())
      .then(data => {
        data = reformatConfig(data);
        this.setState({
          selectedPlugins: {
              [CONFIGURATION_TABS.PROPAGATION]: this.getSelectedPlugins(data, EXPLOITERS_CONFIG_PATH),
              [CONFIGURATION_TABS.CREDENTIALS_COLLECTORS]: this.getSelectedPlugins(data, CREDENTIALS_COLLECTORS_CONFIG_PATH),
              [CONFIGURATION_TABS.PAYLOADS]: this.getSelectedPlugins(data, PAYLOADS_CONFIG_PATH)
          },
          configuration: data,
          currentFormData: _.cloneDeep(data[this.state.selectedSection])
        });
      });
  }

  setSelectedPlugins = (plugins, key) => {
    this.setState({selectedPlugins: {...this.state.selectedPlugins, [key]: plugins}});
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
    let pluginTypes = {
      [CONFIGURATION_TABS.PROPAGATION]: EXPLOITERS_CONFIG_PATH,
      [CONFIGURATION_TABS.CREDENTIALS_COLLECTORS]: CREDENTIALS_COLLECTORS_CONFIG_PATH,
      [CONFIGURATION_TABS.PAYLOADS]: PAYLOADS_CONFIG_PATH
    };
    let config = _.cloneDeep(this.state.configuration)

    for (let pluginType in pluginTypes){
      let pluginPath = pluginTypes[pluginType];
      let pluginFormData = _.get(this.state.configuration, pluginPath);
      let filteredPlugins = {};
      for (let plugin of [...this.state.selectedPlugins[pluginType] ?? []]){
        if (pluginFormData[plugin] === undefined) {
          filteredPlugins[plugin] = {};
        } else {
          filteredPlugins[plugin] = pluginFormData[plugin];
        }
      }
      _.set(config, pluginPath, filteredPlugins)
    }
    return config;
  }

  configSubmit(config) {
    const sendCredentialsPromise = this.sendCredentials();

    const {linuxMasqueBytes, windowsMasqueBytes} = getMasqueradesBytesArrays(this.state.masqueStrings);

    const sendLinuxMasqueStringsPromise = this.sendMasqueStrings(
      APIEndpoint.linuxMasque,
      linuxMasqueBytes
    );

    const sendWindowsMasqueStringsPromise = this.sendMasqueStrings(
      APIEndpoint.windowsMasque,
      windowsMasqueBytes
    );

    Promise.all([sendCredentialsPromise, sendLinuxMasqueStringsPromise, sendWindowsMasqueStringsPromise])
      .then(responses => {
        if (responses.every(res => res?.status === 204)) {
          this.sendConfig(config);
        } else {
          console.log('One or more requests failed.');
        }
      })
      .catch(error => {
        console.log('Error occurred:', error);
      });
  }

  onChange = (formData) => {
    let configuration = this.state.configuration;
    configuration[this.state.selectedSection] = formData;
    this.setState({currentFormData: formData, configuration: configuration});
  };

  onCredentialChange = (credentials) => {
    this.setCredentialsState(credentials.credentialsData, credentials.errors, false);
  }

  onMasqueStringsChange = (masqueStrings) => {
    this.setState({masqueStrings: masqueStrings});
  }


  renderConfigExportModal = () => {
    return (<ConfigExportModal show={this.state.showConfigExportModal}
                               configuration={this.filterUnselectedPlugins()}
                               credentials={this.state.credentials.credentialsData}
                               masqueStrings={this.state.masqueStrings}
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
      },
      true
    )
      .then(res => res.json())
      .then(() => {
          this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL, {method: 'PUT', body: '[]'}, true);
          IslandHttpClient.put(APIEndpoint.linuxMasque, EMPTY_BYTES_ARRAY, true);
          IslandHttpClient.put(APIEndpoint.windowsMasque, EMPTY_BYTES_ARRAY, true);
      })
      .then(() => {
          this.setState({
            lastAction: 'reset'
          });
          this.updateConfig();
          this.props.onStatusChange();
        }
      );
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
        },
        true
      )
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
    let islandCredentials = formatCredentialsForIsland(this.state.credentials.credentialsData);
    let formattedCredentials = JSON.stringify(islandCredentials);
    return (
      this.authFetch(CONFIGURED_PROPAGATION_CREDENTIALS_URL,
        {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: formattedCredentials
        },
        true
      )
        .then(res => {
          if (!res.ok) {
            res.json().then((result) => {
              let errorsId = {};
              let credentialsDataId = {};
              this.state.credentials.credentialsData.forEach((stateCredentials, stateCredentialsIndex) => {
                errorsId[stateCredentials.id] = [];
                credentialsDataId[stateCredentials.id] = stateCredentialsIndex;
                formatCredentialsForIsland([stateCredentials]).forEach((formattedCredentials, _)=> {
                  let indexes = islandCredentials.map((islandCredentialsItem, islandCredentialsIndex) => JSON.stringify(formattedCredentials) === JSON.stringify(islandCredentialsItem) ? islandCredentialsIndex : -1)
                    .filter(islandCredentialsIndex => islandCredentialsIndex !== -1);
                    errorsId[stateCredentials.id].push(indexes[0]);
                })
              });
              this.setState({
                credentialsErrors: result.errors.map(error => {
                  let credentialsErrorId = Object.entries(errorsId).find(([_, credentialsId]) => credentialsId.includes(error.stateCredentialsIndex));
                  let actualRowIndex = credentialsDataId[credentialsErrorId[0]] + 1;
                  return `Credentials Row #${actualRowIndex}: ${error.message.split(', ').pop()}`;
                })
              })
            })
            throw Error()
          }
          return res;
        }).catch((error) => {
        console.log(`bad configuration ${error}`);
        this.setState({lastAction: 'invalid_credentials_configuration'});
      }));
  }

  sendMasqueStrings(endpoint, masqueBytes){
    return IslandHttpClient.put(
      endpoint, masqueBytes, true)
        .then(res => {
        if (res.status !== 204) {
          throw Error();
        }
        return res;
      })
      .catch((error) => {
        console.log(`bad configuration ${error}`);
        this.setState({lastAction: 'invalid_configuration'});
      });
  }

  renderConfigContent = (displayedSchema) => {
    let formProperties = {};
    let fullUiSchema = UiSchema({
      selectedSection: this.state.selectedSection
    });
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
      fullUiSchema,
      formProperties?.schema);
    if (this.state.selectedSection === 'propagation') {
      delete Object.assign(formProperties, {'configuration': formProperties.formData}).formData;
      return (<PropagationConfig {...formProperties}
                                 fullUiSchema={fullUiSchema}
                                 credentials={this.state.credentials}
                                 selectedPlugins={this.state.selectedPlugins}
                                 setSelectedPlugins={this.setSelectedPlugins}
                                 selectedConfigSection={this.state.selectedSection}
                                 onCredentialChange={this.onCredentialChange}/>)
    }
    else if(this.state.selectedSection === 'masquerade'){
      return (<MasqueradeConfig {...formProperties}
                                fullUiSchema={fullUiSchema}
                                masqueStrings={this.state.masqueStrings}
                                onChange={this.onMasqueStringsChange}/>)
    }else {
      formProperties['onChange'] = (formData) => {
        this.onChange(formData.formData)
      };
      return (<FormConfig {...formProperties}
                      fullUiSchema={fullUiSchema}
                      selectedPlugins={this.state.selectedPlugins[this.state.selectedSection]}
                      setSelectedPlugins={this.setSelectedPlugins}
                      selectedSection={this.state.selectedSection}
                      key={displayedSchema.title}/>)
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
    let credentialErrors = this.state.credentials.errors?.length > 0;
    let masqueradeErrors = this.validator.validateFormData(this.state.masqueStrings, MASQUERADE);
    return errors.errors.length+masqueradeErrors.errors.length > 0 || credentialErrors;
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
      displayedSchema['definitions'] = this.state.schema?.['definitions'];
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
          {this.state.lastAction === 'invalid_credentials_configuration' ?
            <div className='alert alert-danger'>
              <FontAwesomeIcon icon={faExclamationCircle} style={{'marginRight': '5px'}}/>
              An invalid configuration file was imported or submitted. The following credentials are invalid:
                  { this.state.credentialsErrors.length !== 0 ?
                    <ul>
                      {this.state.credentialsErrors.map(error => <li key={nanoid()}>{error}</li>)}
                    </ul> : ''
                  }
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
