import React from 'react';
import '../../report-components/security/StolenPasswords'
import StolenPasswordsComponent from '../../report-components/security/StolenPasswords';
import {ScanStatus} from './Helpers'
import MitigationsComponent from './MitigationsComponent';


class T1003 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === ScanStatus.USED ?
          <StolenPasswordsComponent
            data={this.props.data.stolen_creds}/>
          : ''}
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1003;
