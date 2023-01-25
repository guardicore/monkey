import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function mssqlIssueReport(issue) {
  return (
      <>
        Disable the xp_cmdshell option.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
          className="badge badge-danger">MSSQL exploit attack</span>.
          <br/>
          The attack was made possible because the target machine used an outdated MSSQL server configuration allowing
          the usage of the xp_cmdshell command. To learn more about how to disable this feature, read <a
          href="https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option?view=sql-server-2017">
          Microsoft's documentation. </a>
        </CollapsibleWellComponent>
      </>
    );
}
