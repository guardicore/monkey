import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function cdbIssueOverview() {
  return (<li>Apache CouchDB servers are vulnerable to remote code execution.</li>)
}

export function cdbIssueReport(issue) {
  return (
      <>
        Update CouchDB (<a
        href="https://couchdb.apache.org/">
        update</a>).
        <CollapsibleWellComponent>
          The CouchDB server at <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to <span
          className="badge badge-danger">remote code execution</span> attack.
          <br/>
          The attack was made possible due to old version of Apache CouchDB.
        </CollapsibleWellComponent>
      </>
    );
}
