import React, {Component, Fragment} from "react";
import PillarLabel from "./PillarLabel";
import EventsAndButtonComponent from "./EventsAndButtonComponent";
import {ZeroTrustStatuses} from "./ZeroTrustPillars";
import {FindingsTable} from "./FindingsTable";


class FindingsSection extends Component {
  render() {
    return (
      <Fragment>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.failed)} status={ZeroTrustStatuses.failed}/>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.inconclusive)} status={ZeroTrustStatuses.inconclusive}/>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.passed)} status={ZeroTrustStatuses.passed}/>
      </Fragment>
    );
  }

  getFilteredFindings(statusToFilter) {
    const findings = this.props.findings.map((finding) => {
      // Deep copy
      const newFinding = JSON.parse(JSON.stringify(finding));
      if (newFinding.status === statusToFilter) {
        newFinding.pillars = newFinding.pillars.map((pillar) => {
          return {name: pillar, status: this.props.pillarsToStatuses[pillar]}
        });
        return newFinding;
      }
    });
    // Filter nulls out of the list
    return findings.filter(function (el) {
      return el != null;
    });
  }
}


export default FindingsSection;
