import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function sambacryIssueOverview() {
   return (<li>Samba servers are vulnerable to ‘SambaCry’ (<a
                      href="https://www.samba.org/samba/security/CVE-2017-7494.html"
                    >CVE-2017-7494</a>).</li>)
}

export function sambacryIssueReport(issue) {
  return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <br/>
        Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SambaCry</span> attack.
          <br/>
          The Monkey authenticated over the SMB protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password, and used the SambaCry
          vulnerability.
        </CollapsibleWellComponent>
      </>
    );
}
