import React from 'react'
import PieChart from 'react-svg-piechart'

class ScannedBreachedChartComponent extends React.Component {
  constructor() {
    super();

    this.state = {
      expandedSector: null
    };

    this.handleMouseEnterOnSector = this.handleMouseEnterOnSector.bind(this);
  }

  handleMouseEnterOnSector(sector) {
    this.setState({expandedSector: sector});
  }

  render() {
    const data = [
      {label: 'Scanned', value: 4, color: '#f0ad4e'},
      {label: 'Exploited', value: 2, color: '#d9534f'}
    ];

    return (
      <div>
        <PieChart
          data={ data }
          expandedSector={this.state.expandedSector}
          onSectorHover={this.handleMouseEnterOnSector}
          sectorStrokeWidth={2}
        />
        <div>
          {
            data.map((element, i) => (
              <div key={i}>
                <span style={{fontWeight: this.state.expandedSector === i ? 'bold' : null}}>
                  <i className="fa fa-md fa-circle" style={{color: element.color}} /> {element.label} : {element.value}
                </span>
              </div>
            ))
          }
        </div>
      </div>
    )
  }
}

export default ScannedBreachedChartComponent;
