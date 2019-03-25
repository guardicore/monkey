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
    this.state = {lastAction: 'none', matrixData: this.props.configuration};
    // Copy configuration and parse it for ATT&CK matrix table
    let configCopy = JSON.parse(JSON.stringify(this.props.configuration));
    this.maxTechniques = findMaxTechniques(Object.values(configCopy));
    this.data = parseTechniques(Object.values(configCopy), this.maxTechniques);
  }

  getColumns() {
    return Object.keys(this.data[0]).map((key)=>{
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
        body: JSON.stringify(this.state.matrixData)
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

  handleTechniqueChange = (technique, value) => {
    Object.entries(this.state.matrixData).forEach(techType => {
      if(techType[1].properties.hasOwnProperty(technique)){
        let tempMatrix = this.state.matrixData;
        tempMatrix[techType[0]].properties[technique].value = value;
        this.setState({matrixData: tempMatrix});
      }
    });
  };

  render() {
    let columns = this.getColumns();
    return (
      <div className={"attack-matrix"}>
        <form onSubmit={this.onSubmit}>
          <ReactTable
                  columns={columns}
                  data={this.data}
                  showPagination={false}
                  defaultPageSize={this.maxTechniques} />
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
          </div>
        </form>
      </div>);
  }
}

export default MatrixComponent;
