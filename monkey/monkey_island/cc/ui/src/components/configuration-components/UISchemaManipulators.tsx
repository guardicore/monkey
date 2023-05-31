import pluginsManipulator from "./UISchemaPluginsManipulator";

const CREDENTIAL_COLLECTORS_TAB = 'credential_collectors';
const PAYLOADS_TAB = 'payloads';
const PROPAGATION_TAB = 'propagation';


const manipulatorList = [ransomwareDirManipulator, pluginsDirManipulator]

export default function applyUiSchemaManipulators(selectedSection,
                                   formData,
                                   uiSchema,
                                   JSONSchema) {
  for(let i = 0; i < manipulatorList.length; i++){
    manipulatorList[i](selectedSection, formData, uiSchema, JSONSchema);
  }
}

function ransomwareDirManipulator(selectedSection,
                                  formData,
                                  uiSchema) {
  if (selectedSection === PAYLOADS_TAB){
      uiSchema.ransomware.encryption.directories =
        {'ui:disabled': !formData['ransomware']['encryption']['enabled']};
    }
}

function pluginsDirManipulator(selectedSection, formData, uiSchema, JSONSchema) {
  if (selectedSection === PROPAGATION_TAB) {
    pluginsManipulator(uiSchema?.exploitation?.exploiters, JSONSchema?.properties?.exploitation?.properties?.exploiters?.properties)
  } else if (selectedSection === CREDENTIAL_COLLECTORS_TAB) {
    pluginsManipulator(uiSchema?.credentials_collectors, JSONSchema?.properties?.credential_collectors?.properties)
  }
}
