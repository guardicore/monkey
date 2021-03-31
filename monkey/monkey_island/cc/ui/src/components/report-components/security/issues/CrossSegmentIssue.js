import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import {generateInfoBadges} from './utils';

export function crossSegmentIssueOverview() {
  return (<li key="segmentation">Weak segmentation - Machines from
    different segments are able to communicate.</li>)
}

export function generateCrossSegmentIssue(crossSegmentIssue) {
    let crossSegmentIssueOverview = 'Communication possible from '
      + `${crossSegmentIssue['source_subnet']} to ${crossSegmentIssue['target_subnet']}`;

    return (
      <li key={crossSegmentIssueOverview}>
        {crossSegmentIssueOverview}
        <CollapsibleWellComponent>
          <ul className='cross-segment-issues'>
            {crossSegmentIssue['issues'].map(
              issue => generateCrossSegmentIssueListItem(issue)
            )}
          </ul>
        </CollapsibleWellComponent>
      </li>
    );
  }

export function generateCrossSegmentIssueListItem(issue) {
    if (issue['is_self']) {
      return generateCrossSegmentSingleHostMessage(issue);
    }

    return generateCrossSegmentMultiHostMessage(issue);
  }

export function generateCrossSegmentSingleHostMessage(issue) {
    return (
      <li key={issue['hostname']}>
        {`Machine ${issue['hostname']} has both ips: ${issue['source']} and ${issue['target']}`}
      </li>
    );
  }

export function generateCrossSegmentMultiHostMessage(issue) {
    return (
      <li key={issue['source'] + issue['target']}>
        IP {issue['source']} ({issue['hostname']}) was able to communicate with
        IP {issue['target']} using:
        <ul>
          {issue['icmp'] && <li key='icmp'>ICMP</li>}
          {this.generateCrossSegmentServiceListItems(issue)}
        </ul>
      </li>
    );
  }

export function generateCrossSegmentServiceListItems(issue) {
    let service_list_items = [];

    for (const [service, info] of Object.entries(issue['services'])) {
      service_list_items.push(
        <li key={service}>
          <span className='cross-segment-service'>{service}</span> ({info['display_name']})
        </li>
      );
    }

    return service_list_items;
  }

export function generateIslandCrossSegmentIssue(issue) {
    return (
      <>
        Segment your network and make sure there is no communication between machines from different segments.
        <CollapsibleWellComponent>
          The network can probably be segmented. A monkey instance on <span
          className="badge badge-primary">{issue.machine}</span> in the
          networks {generateInfoBadges(issue.networks)}
          could directly access the Monkey Island server in the
          networks {generateInfoBadges(issue.server_networks)}.
        </CollapsibleWellComponent>
      </>
    );
  }
