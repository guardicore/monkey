export function extractExecutionStatusFromServerResponse(res) {
  return {
    allMonkeysAreDead: (!res['completed_steps']['run_monkey']) || (res['completed_steps']['infection_done']),
    runStarted: res['completed_steps']['run_monkey']
  };
}
