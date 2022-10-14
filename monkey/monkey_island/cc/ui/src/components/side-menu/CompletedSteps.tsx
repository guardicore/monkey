export class CompletedSteps {
  runMonkey: boolean
  infectionDone: boolean
  reportDone: boolean
  isLoggedIn: boolean
  needsRegistration: boolean

  public constructor(runMonkey?: boolean,
                     infectinDone?: boolean,
                     reportDone?: boolean) {
    this.runMonkey = runMonkey || false;
    this.infectionDone = infectinDone || false;
    this.reportDone = reportDone || false;
  }

  static buildFromResponse(response: CompletedStepsRequest) {
    return new CompletedSteps(response.run_monkey,
                              response.infection_done,
                              response.report_done);
  }
}

type CompletedStepsRequest = {
  run_monkey: boolean,
  infection_done: boolean,
  report_done: boolean
}
