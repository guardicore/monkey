export const REG_EXP_VALIDATORS = Object.freeze([
  {expression: /[()[\]{};`'"<>]/gmi, expectedTestResult: false},
  {expression: /^([^\w]*)(script|unsafe|javascript|vbscript|app|admin|icloud-sharing|icloud-vetting|help|aim|facetime-audio|applefeedback|ibooks|macappstore|udoc|ts|st|x-apple-helpbasic)/gmi, expectedTestResult: false},
  {expression: /^(?:(?:ht)tps?:|[^a-z]|[a-z+.-]+(?:[^a-z+.\-:]|$))/gmi, expectedTestResult: true}
]);

export const GENERAL_UNSAFE_STRINGS = Object.freeze(['javascript:']);


export const EMPTY_URI = Object.freeze('');
