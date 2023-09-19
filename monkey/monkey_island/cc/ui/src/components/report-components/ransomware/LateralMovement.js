import React from 'react';
import NumberedReportSection from './NumberedReportSection';
import pluralize from 'pluralize'
import BreachedServersComponent from '../security/BreachedServers';
import ExternalLink from '../common/ExternalLink';

const getLateralMovementDescription = () => {
  return (
    <>
      After the initial breach, the attacker will begin the Lateral
      Movement phase of the attack. They will employ various
      techniques in order to compromise other systems in your
      network.
      <br/>
      <br/>
      <ExternalLink
        url="https://www.akamai.com/blog/security/stopping-ransomware-with-segmentation/?utm_medium=monkey-request&utm_source=web-report&utm_campaign=monkey-security-report"
        text="See some real-world examples on Akamai's blog"
      />
    </>
  )
}

function LateralMovement({propagationStats}) {
  const getBody = () => {
    return (
      <>
        {getScannedVsExploitedStats(propagationStats.num_scanned_nodes, propagationStats.num_exploited_nodes)}
        {getExploitationStatsPerExploit(propagationStats.num_exploited_per_exploit)}
        <br/>
        <BreachedServersComponent />
      </>
    )
  }

  return (
    <NumberedReportSection
      index={2}
      title='Lateral Movement'
      description={getLateralMovementDescription()}
      body={getBody()}
    />
  );
}

function getScannedVsExploitedStats(num_scanned_nodes, num_exploited_nodes) {
  return(
    <p>
      Infection Monkey discovered <span className='badge text-bg-warning'>{num_scanned_nodes}</span> machines
      and successfully breached <span className='badge text-bg-danger'>{num_exploited_nodes}</span> of them.
    </p>
  );
}

function getExploitationStatsPerExploit(num_exploited_per_exploit) {
  let exploitation_details = [];

  for (let exploit in num_exploited_per_exploit) {
    let count = num_exploited_per_exploit[exploit];
    exploitation_details.push(
      <div key={exploit}>
        <span className='badge text-bg-danger'>{count}</span>&nbsp;
        {pluralize('machine', count)} {pluralize('was', count)} exploited by the&nbsp;
        <span className='badge text-bg-danger'>{exploit}</span>.
      </div>
    );
  }

  return exploitation_details;
}

export default LateralMovement;
