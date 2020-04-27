import React from 'react';
import MitigationsComponent from './MitigationsComponent';


class T1065 extends React.Component {

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <MitigationsComponent mitigations={this.props.data.mitigations}/>
      </div>
    );
  }
}

export default T1065;
