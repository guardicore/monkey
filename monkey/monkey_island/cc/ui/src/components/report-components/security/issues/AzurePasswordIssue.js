import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function AzurePasswordIssueOverview() {
  return (<li>Azure machines expose plaintext passwords. (<a
                      href="https://www.guardicore.com/2018/03/recovering-plaintext-passwords-azure/"
                    >More info</a>)</li>)
}

export function AzurePasswordIssueReport(issue) {
  return (
      <>
        Delete VM Access plugin configuration files.
        <CollapsibleWellComponent>
          Credentials could be stolen from <span
          className="badge badge-primary">{issue.machine}</span> for the following users <span
          className="badge badge-primary">{issue.users}</span>. Read more about the security issue and remediation <a
          href="https://www.guardicore.com/2018/03/recovering-plaintext-passwords-azure/"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
}
