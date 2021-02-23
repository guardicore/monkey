import React from 'react';

export function ShellShockIssueOverview() {
  return (<li>Machines are vulnerable to ‘Shellshock’ (<a
    href="https://www.cvedetails.com/cve/CVE-2014-6271">CVE-2014-6271</a>).
  </li>)
}


function generateShellshockPathListBadges(paths) {
  return paths.map(path => <span className="badge badge-warning" style={{margin: '2px'}} key={path}>{path}</span>);
}

export function ShellShockIssueReport(issue) {
  return (
    <>
      Update your Bash to a ShellShock-patched version.
      <CollapsibleWellComponent>
        The machine <span className="badge badge-primary">{issue.machine}</span> (<span
        className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
        className="badge badge-danger">ShellShock</span> attack.
        <br/>
        The attack was made possible because the HTTP server running on TCP port <span
        className="badge badge-info">{issue.port}</span> was vulnerable to a shell injection attack on the
        paths: {generateShellshockPathListBadges(issue.paths)}.
      </CollapsibleWellComponent>
    </>
  );
}
