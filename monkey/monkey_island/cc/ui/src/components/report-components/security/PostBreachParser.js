export default function parsePbaResults(results) {
  results.pba_results = aggregateMultipleResultsPba(results.pba_results);
  return results;
}

const SHELL_STARTUP_NAME = 'Modify shell startup file';
const CMD_HISTORY_NAME = 'Clear command history';

function aggregateMultipleResultsPba(results) {
  let aggregatedPbaResults = {
    'Modify shell startup file': {
      aggregatedResult: undefined,
      successfulOutputs: '',
      failedOutputs: '',
      isSuccess: false
    },
    'Clear command history': {
      aggregatedResult: undefined,
      successfulOutputs: '',
      failedOutputs: '',
      isSuccess: false
    }
  }

  function aggregateResults(result) {
    if (aggregatedPbaResults[result.name].aggregatedResult === undefined) {
      aggregatedPbaResults[result.name].aggregatedResult = result;
    }
    if (result.result[1]) {
      aggregatedPbaResults[result.name].successfulOutputs += result.result[0];
      aggregatedPbaResults[result.name].isSuccess = true;
    }
    if (!result.result[1]) {
      aggregatedPbaResults[result.name].failedOutputs += result.result[0];
    }
  }

  function checkAggregatedResults(pbaName) {
    if (aggregatedPbaResults[pbaName].aggregatedResult !== undefined) {
      aggregatedPbaResults[pbaName].aggregatedResult.result[0] = aggregatedPbaResults[pbaName].successfulOutputs + aggregatedPbaResults[pbaName].failedOutputs;
      aggregatedPbaResults[pbaName].aggregatedResult.result[1] = aggregatedPbaResults[pbaName].isSuccess;
      results.push(aggregatedPbaResults[pbaName].aggregatedResult);
    }
  }

  for (let i = 0; i < results.length; i++)
    if (results[i].name === SHELL_STARTUP_NAME || results[i].name === CMD_HISTORY_NAME)
      aggregateResults(results[i]);

  if (aggregatedPbaResults[SHELL_STARTUP_NAME].aggregatedResult === undefined &&
      aggregatedPbaResults[CMD_HISTORY_NAME].aggregatedResult === undefined)
    return results;

  results = results.filter(result => result.name !== SHELL_STARTUP_NAME && result.name !== CMD_HISTORY_NAME);
  checkAggregatedResults(SHELL_STARTUP_NAME);
  checkAggregatedResults(CMD_HISTORY_NAME);

  return results;
}
