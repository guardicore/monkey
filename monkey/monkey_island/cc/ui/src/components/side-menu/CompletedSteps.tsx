export class CompletedSteps {
  runMonkey: boolean;
  infectionDone: boolean;
  reportDone: boolean;

  public constructor(
    runMonkey?: boolean,
    infectionDone?: boolean,
    reportDone?: boolean,
  ) {
    this.runMonkey = runMonkey;
    this.infectionDone = infectionDone;
    this.reportDone = reportDone;
  }
}
