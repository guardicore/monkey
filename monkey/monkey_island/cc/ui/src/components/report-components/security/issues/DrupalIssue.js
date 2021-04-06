import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function drupalIssueOverview() {
  return (<li>Drupal server/s are vulnerable to <a
    href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-6340">CVE-2019-6340</a>.</li>)
}

export function drupalIssueReport(issue) {
  return (
      <>
        Upgrade Drupal server to versions 8.5.11, 8.6.10, or later.
        <CollapsibleWellComponent>
          Drupal server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote command execution</span> attack.
          <br/>
          The attack was made possible because the server is using an old version of Drupal, for which REST API is
          enabled. For possible workarounds, fixes and more info read
          <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-6340">here</a>.
        </CollapsibleWellComponent>
      </>
    );
}
