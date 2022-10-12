export function extractExecutionStatusFromServerResponse(completed_steps_from_server) {
  return {
    allMonkeysAreDead: (!completed_steps_from_server['run_monkey']) || (completed_steps_from_server['infection_done']),
    runStarted: completed_steps_from_server['run_monkey']
  };
}
