export default function parsePbaResults(results) {
  results.pba_results = aggregateMultipleResultsPba(results.pba_results);
  return results;
}

const SHELL_STARTUP_NAME = 'Modify shell startup file';
const CMD_HISTORY_NAME = 'Clear command history';

const multipleResultsPbas = [SHELL_STARTUP_NAME, CMD_HISTORY_NAME]

function aggregateMultipleResultsPba(results) {
  let aggregatedPbaResults = {};
  multipleResultsPbas.forEach(function(pba) {
    aggregatedPbaResults[pba] = {
      aggregatedResult: undefined,
      successfulOutputs: '',
      failedOutputs: '',
      isSuccess: false
    }
  })

  function aggregateResults(result) {
    if (aggregatedPbaResults[result.name].aggregatedResult === undefined) {
      aggregatedPbaResults[result.name].aggregatedResult = result;
    }
    if (result.result[1]) {
      aggregatedPbaResults[result.name].successfulOutputs += result.result[0];
      aggregatedPbaResults[result.name].isSuccess = true;
    }
    else if (!result.result[1]) {
      aggregatedPbaResults[result.name].failedOutputs += result.result[0];
    }
  }

  function checkAggregatedResults(pbaName) {  // if this pba's results were aggregated, push to `results`
    if (aggregatedPbaResults[pbaName].aggregatedResult !== undefined) {
      aggregatedPbaResults[pbaName].aggregatedResult.result[0] = (aggregatedPbaResults[pbaName].successfulOutputs +
                                                                  aggregatedPbaResults[pbaName].failedOutputs);
      aggregatedPbaResults[pbaName].aggregatedResult.result[1] = aggregatedPbaResults[pbaName].isSuccess;
      results.push(aggregatedPbaResults[pbaName].aggregatedResult);
    }
  }

  // check for pbas with multiple results and aggregate their results
  for (let i = 0; i < results.length; i++)
    if (multipleResultsPbas.includes(results[i].name))
      aggregateResults(results[i]);

  // if no modifications were made to the results, i.e. if no pbas had mutiple results, return `results` as it is
  let noResultsModifications = true;
  multipleResultsPbas.forEach((pba) => {
    if (aggregatedPbaResults[pba].aggregatedResult !== undefined)
      noResultsModifications = false;
  })
  if (noResultsModifications)
    return results;

  // if modifications were made, push aggregated results to `results` and return
  results = results.filter(result => !multipleResultsPbas.includes(result.name));
  multipleResultsPbas.forEach(pba => checkAggregatedResults(pba));
  return results;
}
