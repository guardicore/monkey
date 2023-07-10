import React from "react";
import WarningIcon from "../../../ui-components/WarningIcon";
import { Button } from "react-bootstrap";

export function zerologonOverviewWithFailedPassResetWarning() {
  return (
    <span className={"zero-logon-overview-pass-restore-failed"}>
      <WarningIcon />
      Automatic password restoration on a domain controller failed!
      <Button
        variant={"link"}
        href={
          "https://techdocs.akamai.com/infection-monkey/docs/zerologon#manually-restoring-your-password"
        }
        target={"_blank"}
        className={"security-report-link"}
      >
        Restore your domain controller's password manually.
      </Button>
    </span>
  );
}
