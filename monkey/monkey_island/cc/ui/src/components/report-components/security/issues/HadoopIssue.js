import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function HadoopIssueOverview() {
  return (<li>Hadoop/Yarn servers are vulnerable to remote code execution.</li>)
}

export function HadoopIssueReport(issue) {
  return (
      <>
        Run Hadoop in secure mode (<a
        href="http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SecureMode.html">
        add Kerberos authentication</a>).
        <CollapsibleWellComponent>
          The Hadoop server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible due to default Hadoop/Yarn configuration being insecure.
        </CollapsibleWellComponent>
      </>
    );
}
