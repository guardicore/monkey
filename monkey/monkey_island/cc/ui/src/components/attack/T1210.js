import React from 'react';
import '../../styles/Collapse.scss'
import {Link} from "react-router-dom";
import ReactTable from "react-table";


let renderMachine = function (val) {
  return (
    <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
  )
};

let renderPort = function (service){
  if(service.url){
    return service.url
  } else {
    return service.port
  }
};

const columns = [
  {
    columns: [
      {Header: 'Machine', id: 'machine', accessor: x => renderMachine(x), style: { 'whiteSpace': 'unset' }, width: 200},
      {Header: 'Time', id: 'time', accessor: x => x.time, style: { 'whiteSpace': 'unset' }, width: 170},
      {Header: 'Port/url', id: 'port', accessor: x =>renderPort(x), style: { 'whiteSpace': 'unset' }},
      {Header: 'Service', id: 'service', accessor: x => x.service, style: { 'whiteSpace': 'unset' }}
      ]
  }
];

class T1210 extends React.Component {

  constructor(props) {
    super(props);
  }

  renderFoundServices(data) {
    return (
      <div>
        <br/>
        <div>Found services: </div>
        <ReactTable
            columns={columns}
            data={data}
            showPagination={false}
            defaultPageSize={data.length}
        />
      </div>)
  }

  renderExploitedServices(data) {
    return (
      <div>
        <br/>
        <div>Exploited services: </div>
        <ReactTable
            columns={columns}
            data={data}
            showPagination={false}
            defaultPageSize={data.length}
        />
      </div>)
  }

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        {this.props.data.found_services.length > 0 ?
          this.renderFoundServices(this.props.data.found_services) : ''}
        {this.props.data.exploited_services.length > 0 ?
          this.renderExploitedServices(this.props.data.exploited_services) : ''}
        <div className="attack-report footer-text">
          To get more info about scanned and exploited machines view <Link to="/report">standard report.</Link>
        </div>
      </div>
    );
  }
}

export default T1210;
