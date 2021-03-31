import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function struts2IssueOverview() {
  return (<li>Struts2 servers are vulnerable to remote code execution. (<a
                      href="https://cwiki.apache.org/confluence/display/WW/S2-045">
                      CVE-2017-5638</a>)</li>)
}

export function struts2IssueReport(issue) {
  return (
      <>
        Upgrade Struts2 to version 2.3.32 or 2.5.10.1 or any later versions.
        <CollapsibleWellComponent>
          Struts2 server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible because the server is using an old version of Jakarta based file upload
          Multipart parser. For possible work-arounds and more info read <a
          href="https://cwiki.apache.org/confluence/display/WW/S2-045"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
}
