import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function ms08_067IssueOverview() {
  return (<li>Machines are vulnerable to ‘Conficker’ (<a
                      href="https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2008/ms08-067"
  >MS08-067</a>). </li>)
}

export function ms08_067IssueReport(issue) {
  return (
      <>
        Install the latest Windows updates or upgrade to a newer operating system.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">Conficker</span> attack.
          <br/>
          The attack was made possible because the target machine used an outdated and unpatched operating system
          vulnerable to Conficker.
        </CollapsibleWellComponent>
      </>
    );
}
