import React from 'react';
import '../../styles/Collapse.scss'
import {Link} from "react-router-dom";

let renderArray = function(val) {
  return <span>{val.map(x => <span key={x.toString()}> {x} </span>)}</span>;
};


let renderMachine = function (val, index, exploited=false) {
  return (
    <div key={index}>
      {renderArray(val.ip_addresses)}
      {(val.domain_name ? " (".concat(val.domain_name, ")") : " (".concat(val.label, ")"))} :
      {exploited ? renderArray(val.exploits) : renderArray(val.services)}
    </div>
  )
};

class T1210 extends React.Component {

  renderScannedMachines = (machines) => {
    let content = [];
    for (let i = 0; i < machines.length; i++ ){
      if (machines[i].services.length !== 0){
        content.push(renderMachine(machines[i], i))
      }
    }
    return <div>{content}</div>;
  };

  renderExploitedMachines = (machines) => {
    let content = [];
    for (let i = 0; i < machines.length; i++ ){
      if (machines[i].exploits.length !== 0){
        content.push(renderMachine(machines[i], i, true))
      }
    }
    return <div>{content}</div>;
  };

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        {this.props.data.scanned_machines.length > 0 ? <div>Found services: </div> : ''}
        {this.renderScannedMachines(this.props.data.scanned_machines)}
        {this.props.data.exploited_machines.length > 0 ? <div>Successful exploiters:</div> : ''}
        {this.renderExploitedMachines(this.props.data.exploited_machines)}
        <div className="attack-report footer-text">
          To get more info about scanned and exploited machines view <Link to="/report">standard report.</Link>
        </div>
      </div>
    );
  }
}

export default T1210;
