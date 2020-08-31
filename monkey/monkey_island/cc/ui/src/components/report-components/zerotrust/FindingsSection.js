import React, {Component} from 'react';
import {ZeroTrustStatuses} from './ZeroTrustPillars';
import {FindingsTable} from './FindingsTable';


class FindingsSection extends Component {
  mapFindingsByStatus() {
    const statusToFindings = {};
    for (const key in ZeroTrustStatuses) {
      statusToFindings[ZeroTrustStatuses[key]] = [];
    }

    this.props.findings.map((finding) => {
      // Deep copy
      const newFinding = JSON.parse(JSON.stringify(finding));
      newFinding.pillars = newFinding.pillars.map((pillar) => {
        return {name: pillar, status: this.props.pillarsToStatuses[pillar]}
      });
      statusToFindings[newFinding.status].push(newFinding);
    });
    return statusToFindings;
  }

  render() {
    const findingsByStatus = this.mapFindingsByStatus();
    return (
      <div id="findings-section">
        <h2>Findings</h2>
        <p>
          Deep-dive into the details of each test, and see the explicit events and exact timestamps in which things
          happened in your network. This will enable you to match up with your SOC logs and alerts and to gain deeper
          insight as to what exactly happened during this test.
        </p>

        <FindingsTable data={findingsByStatus[ZeroTrustStatuses.failed]} status={ZeroTrustStatuses.failed}/>
        <FindingsTable data={findingsByStatus[ZeroTrustStatuses.verify]} status={ZeroTrustStatuses.verify}/>
        <FindingsTable data={findingsByStatus[ZeroTrustStatuses.passed]} status={ZeroTrustStatuses.passed}/>
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
