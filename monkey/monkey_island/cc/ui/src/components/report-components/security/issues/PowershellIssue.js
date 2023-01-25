import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function powershellIssueReport(issue) {
    return (
      <>
        Restrict PowerShell remote command execution and/or
        harden the credentials of relevant users.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) was
          exploited via <span
          className="badge badge-danger">PowerShell Remoting</span>.
          <br/>
          The attack was made possible because the target machine had
          PowerShell Remoting enabled and Monkey
          had access to correct credentials.
        </CollapsibleWellComponent>
      </>
    );
  }
