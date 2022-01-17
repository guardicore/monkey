import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function log4shellIssueOverview() {
  return (<li>Some servers are vulnerable to the Log4Shell remote code execution exploit.</li>)
}

export function log4shellIssueReport(issue) {
  return (
      <>
        Upgrade the Apache Log4j component to version 2.15.0 or later.
        <CollapsibleWellComponent>
          The {issue.service} server <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}:{issue.port}</span>) is vulnerable to <span
          className="badge badge-danger">the Log4Shell remote code execution</span> attack.
          <br/>
          The attack was made possible due to an old version of Apache Log4j component.
        </CollapsibleWellComponent>
      </>
    );
}
