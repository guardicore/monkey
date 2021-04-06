import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function sshIssueOverview() {
  return (<li>Stolen SSH keys are used to exploit other machines.</li>)
}

export function shhIssueReport(issue) {
  return (
      <>
        Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
        that is not shared with other computers on the network.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SSH</span> attack.
          <br/>
          The Monkey authenticated over the SSH protocol with user <span
          className="badge badge-success">{issue.username}</span> and its password.
        </CollapsibleWellComponent>
      </>
    );
}

export function sshKeysReport(issue) {
    return (
      <>
        Protect <span className="badge badge-success">{issue.ssh_key}</span> private key with a pass phrase.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">SSH</span> attack.
          <br/>
          The Monkey authenticated over the SSH protocol with private key <span
          className="badge badge-success">{issue.ssh_key}</span>.
        </CollapsibleWellComponent>
      </>
    );
  }
