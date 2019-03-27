import React from 'react';
import Checkbox from '../ui-components/checkbox'
import Tooltip from 'react-tooltip-lite'
import AuthComponent from '../AuthComponent';
import ReactTable from "react-table";
import 'filepond/dist/filepond.min.css';
import '../../styles/Tooltip.scss';


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

// Parses config schema into data suitable for react-table (ATT&CK matrix)
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
        if (rowColumn.technique){
          rowColumn.technique.name = Object.keys(techType.properties)[i]
        }
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
    // Copy configuration and parse it for ATT&CK matrix table
    let configCopy = JSON.parse(JSON.stringify(this.props.configuration));
    this.state = {lastAction: 'none',
                  configData: this.props.configuration,
                  maxTechniques: findMaxTechniques(Object.values(configCopy))};
    this.state.matrixTableData = parseTechniques(Object.values(configCopy), this.state.maxTechniques);
    this.state.columns = this.getColumns(this.state.matrixTableData)
  };

  getColumns(matrixData) {
    return Object.keys(matrixData[0]).map((key)=>{
      return {
        Header: key,
        id: key,
        accessor: x => this.renderTechnique(x[key].technique),
        style: { 'whiteSpace': 'unset' }
      };
    });
  }

  renderTechnique(technique) {
    if (technique == null){
      return (<div></div>)
    } else {
      return (<Tooltip content={technique.description} direction="down">
                <Checkbox checked={technique.value}
                          necessary={technique.necessary}
                          name={technique.name}
                          changeHandler={this.handleTechniqueChange}>
                  {technique.title}
                </Checkbox>
              </Tooltip>)
    }
  };

  onSubmit = () => {
    this.authFetch('/api/attack',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(this.state.configData)
      })
      .then(res => {
        if (!res.ok)
        {
          throw Error()
        }
        return res;
      }).then(
        this.setState({
          lastAction: 'saved'
        })
      ).catch(error => {
        console.log('bad configuration');
        this.setState({lastAction: 'invalid_configuration'});
      });
  };

  resetConfig = () => {
    this.authFetch('/api/attack',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify('reset_attack_matrix')
      })
      .then(res => res.json())
      .then(res => {
        this.updateStateFromConfig(res.configuration, 'reset')
      });
  };

  updateStateFromConfig = (config, lastAction = '') => {
    let configCopy = JSON.parse(JSON.stringify(config));
    let maxTechniques = findMaxTechniques(Object.values(configCopy));
    let matrixTableData = parseTechniques(Object.values(configCopy), maxTechniques);
    let columns = this.getColumns(matrixTableData);
    this.setState({
      lastAction: lastAction,
      configData: config,
      maxTechniques: maxTechniques,
      matrixTableData: matrixTableData,
      columns: columns
    });
  };

  handleTechniqueChange = (technique, value, mapped=false) => {
    // Change value on configuration
    Object.entries(this.state.configData).forEach(techType => {
      if(techType[1].properties.hasOwnProperty(technique)){
        let tempMatrix = this.state.configData;
        tempMatrix[techType[0]].properties[technique].value = value;
        // Toggle all mapped techniques
        if (! mapped && tempMatrix[techType[0]].properties[technique].hasOwnProperty('mapped_to')){
          console.log("Triggered");
          tempMatrix[techType[0]].properties[technique].mapped_to.forEach(mappedTechnique => {
            console.log(mappedTechnique)
            this.handleTechniqueChange(mappedTechnique, value, true)
          })
        }
        this.updateStateFromConfig(tempMatrix);
      }
    });

  };

  render() {
    return (
      <div className={"attack-matrix"}>
        <form onSubmit={this.onSubmit}>
          <ReactTable
                  columns={this.state.columns}
                  data={this.state.matrixTableData}
                  showPagination={false}
                  defaultPageSize={this.state.maxTechniques} />
          <div className={"messages"}>
            { this.state.lastAction === 'reset' ?
              <div className="alert alert-success">
                <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
                Matrix reset to default.
              </div>
              : ''}
            { this.state.lastAction === 'saved' ?
              <div className="alert alert-success">
                <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
                Matrix applied to configuration.
              </div>
              : ''}
            { this.state.lastAction === 'invalid_configuration' ?
              <div className="alert alert-danger">
                <i className="glyphicon glyphicon-exclamation-sign" style={{'marginRight': '5px'}}/>
                An invalid matrix configuration supplied, check selected fields.
              </div>
              : ''}
          </div>
          <div className="text-center">
            <button type="button" onClick={this.onSubmit} className="btn btn-success btn-lg" style={{margin: '5px'}}>
              Apply to configuration
            </button>
            <button type="button" onClick={this.resetConfig} className="btn btn-danger btn-lg" style={{margin: '5px'}}>
              Reset to default matrix
            </button>
          </div>
        </form>
      </div>);
  }
}

export default MatrixComponent;
