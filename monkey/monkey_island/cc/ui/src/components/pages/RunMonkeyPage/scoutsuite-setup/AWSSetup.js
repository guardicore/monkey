import {Button} from 'react-bootstrap';
import React from 'react';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import CloudOptions from './CloudOptions';
import {COLUMN_SIZES} from '../../../ui-components/inline-selection/utils';
import '../../../../styles/components/scoutsuite/AWSSetup.scss';

export default function AWSSetup(props) {
  return InlineSelection(getContents, {
    ...props,
    collumnSize: COLUMN_SIZES.LARGE,
    onBackButtonClick: () => {
      props.setComponent(CloudOptions, props)
    }
  })
}


const getContents = (props) => {
  return (
    <div className={'aws-scoutsuite-configuration'}>
      <h2>ScoutSuite configuration for AWS</h2>
      <p>To assess your AWS infrastructure's security do the following:</p>
      <ol>
        <li>
          1. Configure AWS CLI on Monkey Island Server (if you already have a configured CLI you can skip this step).
          <ol className={'nested-ol'}>
            <li>
              1. Download <Button href={'https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html'}
                                  target={'_blank'} variant={'link'}>AWS CLI</Button> and
              install it on the Monkey Island server (machine running this page).
            </li>
            <li>
              2. Run <code>aws configure</code>. It's important to configure credentials, which
              allows ScoutSuite to get information about your cloud configuration. The most trivial way to do so is to
              provide <Button
              href={'https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds'}
              variant={'link'}>
              Access key ID and secret access key
            </Button>.
            </li>
          </ol>
        </li>
        <li>
          2. If you change the configuration, make sure not to disable AWS system info collector.
        </li>
        <li>
          3. Go back and run Monkey on the Island server.
        </li>
        <li>
          4. Assess results in Zero Trust report.
        </li>
      </ol>
    </div>
  );
}
