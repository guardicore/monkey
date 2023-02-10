
const manipulatorList = [ransomwareDirManipulator]

function applyUiSchemaManipulators(selectedSection,
                                   formData,
                                   uiSchema) {
  for(let i = 0; i < manipulatorList.length; i++){
    manipulatorList[i](selectedSection, formData, uiSchema);
  }
}

function ransomwareDirManipulator(selectedSection,
                                  formData,
                                  uiSchema) {
  if (selectedSection === 'payloads'){
      uiSchema.encryption.directories =
        {'ui:disabled': !formData['encryption']['enabled']};
    }
}

export default applyUiSchemaManipulators;
