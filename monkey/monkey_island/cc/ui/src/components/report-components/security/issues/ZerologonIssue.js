import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import WarningIcon from '../../../ui-components/WarningIcon';
import {Button} from 'react-bootstrap';

export function zerologonIssueOverview() {
  return (
    <li>
      Some Windows domain controllers are vulnerable to 'Zerologon' (
      <Button variant={'link'}
              href='https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-1472'
              target={'_blank'}
              className={'security-report-link'}>
        CVE-2020-1472
      </Button>).
    </li>
  )
}

export function zerologonOverviewWithFailedPassResetWarning() {
  let overview = [zerologonIssueOverview()];
  overview.push(
    <li>
      <span className={'zero-logon-overview-pass-restore-failed'}>
        <WarningIcon/>
        Automatic password restoration on a domain controller failed!
        <Button variant={'link'}
                href={'https://www.guardicore.com/infectionmonkey/docs/reference/exploiters/zerologon/'}
                target={'_blank'}
                className={'security-report-link'}>
          Restore your domain controller's password manually.
        </Button>
      </span>
    </li>
  )
  return overview;
}

export function zerologonIssueReport(issue) {
  return (
    <>
      Install Windows security updates.
      <CollapsibleWellComponent>
        The machine <span className="badge badge-primary">{issue.machine}</span> (<span
        className="badge badge-info" style={{margin: '2px'}}>{issue.ip_address}</span>) is vulnerable to a <span
        className="badge badge-danger">Zerologon exploit</span>.
        <br/>
        The attack was possible because the latest security updates from Microsoft
        have not been applied to this machine. For more information about this
        vulnerability, read <a href="https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-1472">
        Microsoft's documentation.</a>
        {!issue.password_restored ?
          <div className={'info-pane-warning'} key={'warning'}>
            <br/><WarningIcon/>
            <span>
              The domain controller's password was changed during the exploit and could not be restored successfully.
              Instructions on how to manually reset the domain controller's password can be found <a
              href="https://www.guardicore.com/infectionmonkey/docs/reference/exploiters/zerologon/">here</a>.
            </span>
          </div> : null}
      </CollapsibleWellComponent>
    </>
  );
}
