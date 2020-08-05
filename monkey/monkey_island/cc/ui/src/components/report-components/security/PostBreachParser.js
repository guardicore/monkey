export default function parsePbaResults(results) {
  results.pba_results = aggregateShellStartupPba(results.pba_results);
  return results;
}

const SHELL_STARTUP_NAME = 'Modify shell startup file';

function aggregateShellStartupPba(results) {
  let isSuccess = false;
  let aggregatedPbaResult = undefined;
  let successfulOutputs = '';
  let failedOutputs = '';

  for(let i = 0; i < results.length; i++){
    if(results[i].name === SHELL_STARTUP_NAME && aggregatedPbaResult === undefined){
      aggregatedPbaResult = results[i];
    }
    if(results[i].name === SHELL_STARTUP_NAME && results[i].result[1]){
      successfulOutputs += results[i].result[0];
      isSuccess = true;
    }
    if(results[i].name === SHELL_STARTUP_NAME && ! results[i].result[1]){
      failedOutputs += results[i].result[0];
    }
  }
  if(aggregatedPbaResult === undefined) return results;

  results = results.filter(result => result.name !== SHELL_STARTUP_NAME);
  aggregatedPbaResult.result[0] = successfulOutputs + failedOutputs;
  aggregatedPbaResult.result[1] = isSuccess;
  results.push(aggregatedPbaResult);
  return results;
}
