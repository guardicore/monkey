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
                     reportDone?: boolean,
                     isLoggedIn?: boolean,
                     needsRegistration?: boolean) {
    this.runServer = runServer || false;
    this.runMonkey = runMonkey || false;
    this.infectionDone = infectinDone || false;
    this.reportDone = reportDone || false;
    this.isLoggedIn = isLoggedIn || false;
    this.needsRegistration = needsRegistration || false;
  }
}
