import React, {Component} from 'react';
import * as PropTypes from 'prop-types';
import ResponsiveVennDiagram from './venn-components/ResponsiveVennDiagram';

class PillarOverview extends Component {
  render() {
    return (<div id={this.constructor.name}>
      <ResponsiveVennDiagram pillarsGrades={this.props.grades}/>
    </div>);
  }
}

export default PillarOverview;

PillarOverview.propTypes = {
  grades: PropTypes.array
};
