import React, {Component, Fragment} from "react";
import PillarLabel from "./PillarLabel";
import EventsButton from "./EventsButton";
import {ZeroTrustStatuses} from "./ZeroTrustPillars";
import {FindingsTable} from "./FindingsTable";


class FindingsSection extends Component {
  render() {
    return (
      <div id="findings-section">
        <h2>Findings</h2>
        <p>
          Deep-dive into the details of each test, and see the explicit events and exact timestamps in which things
          happened in your network. This will enable you to match up with your SOC logs and alerts and to gain deeper
          insight as to what exactly happened during this test.
        </p>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.failed)} status={ZeroTrustStatuses.failed}/>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.inconclusive)} status={ZeroTrustStatuses.inconclusive}/>
        <FindingsTable data={this.getFilteredFindings(ZeroTrustStatuses.passed)} status={ZeroTrustStatuses.passed}/>
      </div>
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
