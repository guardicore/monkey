import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import { Button } from 'react-bootstrap';

export function log4shellIssueReport(issue) {
  return (
    <>
      Upgrade the Apache Log4j component to version 2.15.0 or later.
      <CollapsibleWellComponent>
        The server <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{ margin: '2px' }}>{issue.ip_address}</span>) is vulnerable to <span
            className="badge badge-danger">the Log4Shell remote code execution</span> attack.
        <br />
        The attack was made possible due to an old version of Apache Log4j component (
        <Button
          variant={'link'}
          href='https://cve.mitre.org/cgi-bin/cvename.cgi?name=2021-44228'
          target={'_blank'}
          className={'security-report-link'}
        >
          CVE-2021-44228
        </Button>).
      </CollapsibleWellComponent>
    </>
  );
}
