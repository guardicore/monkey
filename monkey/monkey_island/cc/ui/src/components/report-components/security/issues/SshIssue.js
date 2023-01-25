import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

port function shhIssueReport(issue) {
  return (
    <>
      Change user passwords to a complex one-use password that is not shared with other computers on the network.
      Protect private keys with a pass phrase.
      <CollapsibleWellComponent>
        The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{ margin: '2px' }}>{issue.ip_address}</span>) is vulnerable to an <span
            className="badge badge-danger">SSH</span> attack.
        <br />
        The Monkey authenticated over the SSH protocol.
      </CollapsibleWellComponent>
    </>
  );
}
