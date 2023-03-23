import {EMPTY_URI, GENERAL_UNSAFE_STRINGS, REG_EXP_VALIDATORS} from './uriSanitizer.constants';

export const sanitizeURI = (uri) => {
  const validators =  REG_EXP_VALIDATORS;
  for(let i=0; i < validators.length; i++){
    const regTest = new RegExp(validators[i].expression);
    if(regTest.test(uri) !== validators[i].expectedTestResult) {
      return EMPTY_URI;
    }
  }

  for(let i=0; i < GENERAL_UNSAFE_STRINGS.length; i++){
    if(uri.indexOf(GENERAL_UNSAFE_STRINGS[i]) !== -1){
      return EMPTY_URI;
    }
  }

  return uri;
}
