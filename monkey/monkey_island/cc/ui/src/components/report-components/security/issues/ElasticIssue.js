import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function ElasticIssueOverview() {
  return (<li>Elasticsearch servers are vulnerable to <a
                      href="https://www.cvedetails.com/cve/cve-2015-1427">CVE-2015-1427</a>.
                    </li>)
}

export function ElasticIssueReport(issue) {
  return (
      <>
        Update your Elastic Search server to version 1.4.3 and up.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to an <span
          className="badge badge-danger">Elastic Groovy</span> attack.
          <br/>
          The attack was made possible because the Elastic Search server was not patched against CVE-2015-1427.
        </CollapsibleWellComponent>
      </>
    );
}
