import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function tunnelIssueOverview(){
  return (<li key="tunnel">Weak segmentation - Machines were able to communicate over unused ports.</li>)
}

export function tunnelIssueReport(issue) {
    return (
      <>
        Use micro-segmentation policies to disable communication other than the required.
        <CollapsibleWellComponent>
          Machines are not locked down at port level. Network tunnel was set up from <span
          className="badge badge-primary">{issue.agent_machine}</span> to <span
          className="badge badge-primary">{issue.agent_tunnel}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }
