import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';

export function strongUsersOnCritIssueReport(issue) {
    return (
      <>
        This critical machine is open to attacks via strong users with access to it.
        <CollapsibleWellComponent>
          The services: {this.generateInfoBadges(issue.services)} have been found on the machine
          thus classifying it as a critical machine.
          These users has access to it:
          {this.generateInfoBadges(issue.threatening_users)}.
        </CollapsibleWellComponent>
      </>
    );
  }
