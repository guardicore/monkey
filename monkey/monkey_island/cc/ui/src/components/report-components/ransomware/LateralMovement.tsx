import React, {ReactElement} from 'react';
import NumberedReportSection from './NumberedReportSection';
import pluralize from 'pluralize'

const LATERAL_MOVEMENT_DESCRIPTION = 'After the initial breach, the attacker will begin the Lateral \
                                      Movement phase of the attack. They will employ various \
                                      techniques in order to compromise other systems in your \
                                      network and encrypt as many files as possible.'

type PropagationStats = {
  num_scanned_nodes: number,
  num_exploited_nodes: number,
  num_exploited_per_exploit: Array<number>,
}

function LateralMovement({propagationStats}: {propagationStats: PropagationStats}): ReactElement {
  let body = (
    <>
      {getScannedVsExploitedStats(propagationStats.num_scanned_nodes, propagationStats.num_exploited_nodes)}
      {getExploitationStatsPerExploit(propagationStats.num_exploited_per_exploit)}
    </>
  )

  return (
    <NumberedReportSection
      index={2}
      title='Lateral Movement'
      description={LATERAL_MOVEMENT_DESCRIPTION}
      body={body}
    />
  );
}

function getScannedVsExploitedStats(num_scanned_nodes: number, num_exploited_nodes: number): ReactElement {
  return(
    <p>
      The Monkey discovered <span className='badge badge-warning'>{num_scanned_nodes}</span> machines
      and successfully breached <span className='badge badge-danger'>{num_exploited_nodes}</span> of them.
    </p>
  );
}

function getExploitationStatsPerExploit(num_exploited_per_exploit: Array<number>): Array<ReactElement> {
  let exploitation_details = [];

  for (let exploit in num_exploited_per_exploit) {
    let count = num_exploited_per_exploit[exploit];
    exploitation_details.push(
      <div key={exploit}>
        <span className='badge badge-danger'>{count}</span>&nbsp;
        {pluralize('machine', count)} {pluralize('was', count)} exploited by the&nbsp;
        <span className='badge badge-danger'>{exploit}</span>.
      </div>
    );
  }

  return exploitation_details;
}

export default LateralMovement;
