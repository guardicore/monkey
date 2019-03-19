import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';
import CheckBox from '../ui-components/checkBox'
import AuthComponent from '../AuthComponent';
import 'filepond/dist/filepond.min.css';
import ReactTable from "react-table";


let renderTechnique = function (technique) {
  console.log(technique);
  if (technique == null){
    return (<div></div>)
  } else {
    return (<div>{technique.title}</div>)
  }
};

// Finds which attack type has most techniques and returns that number
let findMaxTechniques =  function (data){
  let maxLen = 0;
  data.forEach(function(techType) {
    if (Object.keys(techType.properties).length > maxLen){
      maxLen = Object.keys(techType.properties).length
    }
  });
  return maxLen
};

let parseTechniques = function (data, maxLen) {
  let techniques = [];
  // Create rows with attack techniques
  for (let i = 0; i < maxLen; i++) {
    let row = {};
    data.forEach(function(techType){
      let rowColumn = {};
      rowColumn.techName = techType.title;
      if (i <= Object.keys(techType.properties).length) {
        rowColumn.technique = Object.values(techType.properties)[i];
      } else {
        rowColumn.technique = null
      }
      row[rowColumn.techName] = rowColumn
    });
    techniques.push(row)
  }
  return techniques;
};

class MatrixComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.maxTechniques = findMaxTechniques(Object.values(this.props.configuration));
    this.data = parseTechniques(Object.values(this.props.configuration), this.maxTechniques);
  }

  getColumns() {
    return Object.keys(this.data[0]).map((key)=>{
      return {
        Header: key,
        id: key,
        accessor: x => renderTechnique(x[key].technique)
      };
    });
  }

  render() {
    console.log(this.data);
    let columns = this.getColumns();
    return (<ReactTable
                columns={columns}
                data={this.data}
                showPagination={false}
                defaultPageSize={this.maxTechniques}
              />);
  }
}

export default MatrixComponent;
