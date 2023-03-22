const REG_EXP_VALIDATORS = Object.freeze([
    {expression: /[()[\]{};`'"<>]/gmi, expectedTestResult: false},
    {expression: /^([^\w]*)(script|unsafe|javascript|vbscript|app|admin|icloud-sharing|icloud-vetting|help|aim|facetime-audio|applefeedback|ibooks|macappstore|udoc|ts|st|x-apple-helpbasic)/gmi, expectedTestResult: false},
    {expression: /^(?:(?:(?:f|ht)tps?):|[^a-z]|[a-z+.-]+(?:[^a-z+.\-:]|$))/gmi, expectedTestResult: true}
]);

const GENERAL_UNSAFE_STRINGS = Object.freeze(['javascript:']);

export const sanitizeURI = (uri) => {
  const EMPTY_URI = '';

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
