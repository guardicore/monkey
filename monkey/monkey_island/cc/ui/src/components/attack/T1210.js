import React from 'react';
import ReactTable from 'react-table'
import '../../styles/Collapse.scss'
import Collapse from '@kunukn/react-collapse';

let renderArray = function(val) {
  return <div>{val.map(x => <div>{x}</div>)}</div>;
};

let renderIpAddresses = function (val) {
  return <div>{renderArray(val.ip_addresses)} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")} </div>;
};

const columns = [
];

const pageSize = 10;

class T1210 extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    console.log(this.props);
    return (
      <Collapse isOpen={true || false}>
        <div>{this.props.data.message}</div>
      </Collapse>
    );
  }
}

export default T1210;
