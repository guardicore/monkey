export class CompletedSteps {
  runMonkey: boolean
  infectionDone: boolean
  reportDone: boolean

  public constructor(runMonkey?: boolean,
                     infectionDone?: boolean,
                     reportDone?: boolean) {
    this.runMonkey = runMonkey || false;
    this.infectionDone = infectionDone || false;
    this.reportDone = reportDone || false;
  }
}
