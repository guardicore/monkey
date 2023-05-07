import pluginsManipulator from "./UISchemaPluginsManipulator";

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
  if (selectedSection === 'payloads'){
      uiSchema.ransomware.encryption.directories =
        {'ui:disabled': !formData['ransomware']['encryption']['enabled']};
    }
}

function pluginsDirManipulator(selectedSection, formData, uiSchema, JSONSchema) {
  if(selectedSection === 'propagation') {
    pluginsManipulator(uiSchema?.exploitation?.exploiters, JSONSchema?.properties?.exploitation?.properties?.exploiters?.properties)
  }
}
