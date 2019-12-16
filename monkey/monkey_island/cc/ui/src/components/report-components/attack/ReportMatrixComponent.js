import React from 'react';

import Checkbox from '../../ui-components/Checkbox';
import ReactTable from 'react-table';
import 'filepond/dist/filepond.min.css';
import '../../../styles/report/ReportAttackMatrix.scss';

class ReportMatrixComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {techniques: this.props.techniques,
                  schema: this.props.schema};
  }

  getColumns() {
    let columns = [];
    for(const type_key in this.state.schema.properties){
      if (! this.state.schema.properties.hasOwnProperty(type_key)){
        continue;
      }
      let tech_type = this.state.schema.properties[type_key];
      columns.push({
        Header: () => (<a href={tech_type.link} target="_blank">{tech_type.title}</a>),
        id: type_key,
        accessor: x => this.renderTechnique(x[tech_type.title]),
        style: {'whiteSpace': 'unset'}
      });
    }
    return columns;
  }

  getTableRows() {
    let rows = [];
    for (const tech_id in this.state.techniques) {
      if (this.state.techniques.hasOwnProperty(tech_id)){
        let technique_added = false;
        let technique = this.state.techniques[tech_id];
        for(const row of rows){
          if (! row.hasOwnProperty(technique.type)){
            row[technique.type] = technique;
            technique_added = true;
            break;
          }
        }
        if (! technique_added){
          let newRow = {};
          newRow[technique.type] = technique;
          rows.push(newRow)
        }
      }
    }
    return rows;
  }

  renderTechnique(technique) {
    if (technique == null || typeof technique === undefined) {
      return (<div/>)
    } else {
      return (
        <Checkbox checked={technique.selected}
                  necessary={false}
                  name={technique.title}
                  changeHandler={this.props.onClick}
                  status={technique.status}>
          {technique.title}
        </Checkbox>)
    }
  }

  render() {
    let tableRows = this.getTableRows();
    return (
      <div>
        <div className={'attack-matrix'}>
          <ReactTable columns={this.getColumns()}
                      data={tableRows}
                      showPagination={false}
                      defaultPageSize={tableRows.length}/>
        </div>
      </div>);
  }
}

export default ReportMatrixComponent;
