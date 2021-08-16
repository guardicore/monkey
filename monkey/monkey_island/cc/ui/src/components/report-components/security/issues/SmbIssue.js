import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function smbPasswordReport(issue) {
  return (
    <>
      Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
      that is not shared with other computers on the network.
      <CollapsibleWellComponent>
        The machine <span className="badge badge-primary">{issue.machine}</span> (<span
        className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
        className="badge badge-danger">SMB</span> attack.
        <br/>
        The Monkey authenticated over the SMB protocol with user <span
        className="badge badge-success">{issue.username}</span> and its password.
      </CollapsibleWellComponent>
    </>
  );
}

export function smbPthReport(issue) {
  return (
    <>
      Change <span className="badge badge-success">{issue.username}</span>'s password to a complex one-use password
      that is not shared with other computers on the network.
      <CollapsibleWellComponent>
        The machine <span className="badge badge-primary">{issue.machine}</span> (<span
        className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
        className="badge badge-danger">SMB</span> attack.
        <br/>
        The Monkey used a pass-the-hash attack over SMB protocol with user <span
        className="badge badge-success">{issue.username}</span>.
      </CollapsibleWellComponent>
    </>
  );
}
