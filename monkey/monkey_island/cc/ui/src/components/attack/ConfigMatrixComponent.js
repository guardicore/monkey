import React from 'react';
import Checkbox from '../ui-components/Checkbox'
import Tooltip from 'react-tooltip-lite'
import AuthComponent from '../AuthComponent';
import ReactTable from 'react-table';
import 'filepond/dist/filepond.min.css';
import '../../styles/components/Tooltip.scss';
import {Col} from 'react-bootstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle as faCircle } from '@fortawesome/free-solid-svg-icons/faCircle';
import { faCircle as faCircleThin } from '@fortawesome/free-regular-svg-icons/faCircle';

class ConfigMatrixComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {lastAction: 'none'}
  }

  // Finds which attack type has most techniques and returns that number
  static findMaxTechniques(data) {
    let maxLen = 0;
    data.forEach(function (techType) {
      if (Object.keys(techType.properties).length > maxLen) {
        maxLen = Object.keys(techType.properties).length
      }
    });
    return maxLen
  }

  // Parses ATT&CK config schema into data suitable for react-table (ATT&CK matrix)
  static parseTechniques(data, maxLen) {
    let techniques = [];
    // Create rows with attack techniques
    for (let i = 0; i < maxLen; i++) {
      let row = {};
      data.forEach(function (techType) {
        let rowColumn = {};
        rowColumn.techName = techType.title;

        if (i <= Object.keys(techType.properties).length) {
          rowColumn.technique = Object.values(techType.properties)[i];
          if (rowColumn.technique) {
            rowColumn.technique.name = Object.keys(techType.properties)[i];
          }
        } else {
          rowColumn.technique = null;
        }
        row[rowColumn.techName] = rowColumn;
      });
      techniques.push(row)
    }
    return techniques;
  }

  getColumns(matrixData) {
    return Object.keys(matrixData[0]).map((key) => {
      return {
        Header: key,
        id: key,
        accessor: x => this.renderTechnique(x[key].technique),
        style: {'whiteSpace': 'unset'}
      };
    });
  }

  renderTechnique(technique) {
    if (technique == null) {
      return (<div/>)
    } else {
      return (<Tooltip content={technique.description} direction="down">
        <Checkbox checked={technique.value}
                  necessary={technique.necessary}
                  name={technique.name}
                  changeHandler={this.props.change}>
          {technique.title}
        </Checkbox>
      </Tooltip>)
    }
  }

  getTableData = (config) => {
    let configCopy = JSON.parse(JSON.stringify(config));
    let maxTechniques = ConfigMatrixComponent.findMaxTechniques(Object.values(configCopy));
    let matrixTableData = ConfigMatrixComponent.parseTechniques(Object.values(configCopy), maxTechniques);
    let columns = this.getColumns(matrixTableData);
    return {'columns': columns, 'matrixTableData': matrixTableData, 'maxTechniques': maxTechniques}
  };

  renderLegend = () => {
    return (
      <div id="header" className="row justify-content-between attack-legend">
        <Col xs={4}>
          <FontAwesomeIcon icon={faCircleThin} className="icon-unchecked"/>
          <span> - Disabled</span>
        </Col>
        <Col xs={4}>
          <FontAwesomeIcon icon={faCircle} className="icon-checked"/>
          <span> - Enabled</span>
        </Col>
        <Col xs={4}>
          <FontAwesomeIcon icon={faCircle} className="icon-mandatory"/>
          <span> - Mandatory</span>
        </Col>
      </div>)
  };

  render() {
    let tableData = this.getTableData(this.props.configuration);
    return (
      <div>
        {this.renderLegend()}
        <div className={'attack-matrix'}>
          <ReactTable columns={tableData['columns']}
                      data={tableData['matrixTableData']}
                      showPagination={false}
                      defaultPageSize={tableData['maxTechniques']}/>
        </div>
      </div>);
  }
}

export default ConfigMatrixComponent;
