import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function vsftpdIssueOverview() {
  return (<li>VSFTPD is vulnerable to <a
                      href="https://www.rapid7.com/db/modules/exploit/unix/ftp/vsftpd_234_backdoor">CVE-2011-2523</a>.
                    </li>)
}

export function vsftpdIssueReport(issue) {
  return (
      <>
        Update your VSFTPD server to the latest version vsftpd-3.0.3.
        <CollapsibleWellComponent>
          The machine <span className="badge badge-primary">{issue.machine}</span> (<span
          className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) has a backdoor running at
          port <span
          className="badge badge-danger">6200</span>.
          <br/>
          The attack was made possible because the VSFTPD server was not patched against CVE-2011-2523.
          <br/><br/>In July 2011, it was discovered that vsftpd version 2.3.4 downloadable from the master site had been
          compromised.
          Users logging into a compromised vsftpd-2.3.4 server may issue a ":)" smileyface as the username and gain a
          command
          shell on port 6200.
          <br/><br/>
          The Monkey executed commands by first logging in with ":)" in the username and then sending commands to the
          backdoor
          at port 6200.
          <br/><br/>Read more about the security issue and remediation <a
          href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-2523"
        >here</a>.
        </CollapsibleWellComponent>
      </>
    );
}
