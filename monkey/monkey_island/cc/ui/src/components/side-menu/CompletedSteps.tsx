export class CompletedSteps {
  runServer: boolean
  runMonkey: boolean
  infectionDone: boolean
  reportDone: boolean
  isLoggedIn: boolean
  needsRegistration: boolean

  public constructor(runServer?: boolean,
                     runMonkey?: boolean,
                     infectinDone?: boolean,
                     reportDone?: boolean) {
    this.runServer = runServer || false;
    this.runMonkey = runMonkey || false;
    this.infectionDone = infectinDone || false;
    this.reportDone = reportDone || false;
  }

  static buildFromResponse(response: CompletedStepsRequest) {
    return new CompletedSteps(response.run_server,
                              response.run_monkey,
                              response.infection_done,
                              response.report_done);
  }
}

type CompletedStepsRequest = {
  run_server: boolean,
  run_monkey: boolean,
  infection_done: boolean,
  report_done: boolean
}
