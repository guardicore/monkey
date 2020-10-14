import {Button} from 'react-bootstrap';
import React from 'react';
import InlineSelection from '../../../../ui-components/inline-selection/InlineSelection';
import {COLUMN_SIZES} from '../../../../ui-components/inline-selection/utils';
import '../../../../../styles/components/scoutsuite/AWSSetup.scss';
import AWSSetupOptions from './AWSSetupOptions';


export default function AWSCLISetup(props) {
  return InlineSelection(getContents, {
    ...props,
    collumnSize: COLUMN_SIZES.LARGE,
    onBackButtonClick: () => {
      props.setComponent(AWSSetupOptions, props);
    }
  })
}


const getContents = (props) => {
  return (
    <div className={'aws-scoutsuite-configuration'}>
      <h2>AWS CLI configuration for scan</h2>
      <p>To assess your AWS infrastructure's security do the following:</p>
      <ol>
        <li>
          1. Configure AWS CLI on Monkey Island Server (if you already have a configured CLI you can skip this step).
          <ol className={'nested-ol'}>
            <li>
              a. Download <Button href={'https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html'}
                                  target={'_blank'} variant={'link'}>AWS CLI</Button> and
              install it on the Monkey Island server (machine running this page).
            </li>
            <li>
              b. Run <code>aws configure</code>. It's important to configure credentials as it
              allows ScoutSuite to get information about your cloud configuration. The simplest way to do so is to
              provide&nbsp;
              <Button
                href={'https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds'}
                variant={'link'}
                className={'cli-link'}
                target={'_blank'}>
              Access key ID and secret access key
            </Button>.
            </li>
          </ol>
        </li>
        <li>
          2. If you change the configuration, make sure not to disable AWS system info collector.
        </li>
        <li>
          3. Go <Button onClick={() => props.setComponent()}
                        variant={'link'}
                        className={'cli-link'}>back</Button>
          &nbsp;and run Monkey on the Island server.
        </li>
        <li>
          4. Assess results in Zero Trust report.
        </li>
      </ol>
    </div>
  );
}
