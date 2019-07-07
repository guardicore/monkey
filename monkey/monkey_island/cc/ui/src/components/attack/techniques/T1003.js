import React from 'react';
import '../../../styles/Collapse.scss'
import '../../report-components/StolenPasswords'
import StolenPasswordsComponent from "../../report-components/StolenPasswords";


class T1003 extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === 'USED' ?
          <StolenPasswordsComponent data={this.props.reportData.glance.stolen_creds.concat(this.props.reportData.glance.ssh_keys)}/>
          : ""}
      </div>
    );
  }
}

export default T1003;
