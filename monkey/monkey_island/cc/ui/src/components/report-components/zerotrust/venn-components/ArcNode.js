import React from 'react'
import PropTypes from 'prop-types';
import {Popover, OverlayTrigger} from 'react-bootstrap';
import * as d3 from 'd3'

class ArcNode extends React.Component {
  render() {
    let {prefix, index, data} = this.props;

    let arc = d3.arc().innerRadius(data.inner).outerRadius(data.outer).startAngle(0).endAngle(Math.PI * 2.0);
    let id = prefix + 'Node_' + index;

    return (
      <OverlayTrigger key={prefix + 'arcGroup' + index} trigger={['hover', 'focus']} placement={data.popover}
                      overlay={<Popover key={prefix + 'ArcTooltip' + index} id={prefix + 'Popover' + index}
                                        style={{backgroundColor: data.hex}}
                                        title={data.node.pillar}>{data.tooltip}</Popover>}>
        <g transform={'rotate(180)'} id={data.node.pillar} key={prefix + 'arcGroup' + index}>
          <path

            id={prefix + 'Node_' + index}
            className={'arcNode'}
            data-tooltip={data.tooltip}
            d={arc()}
            fill={data.hex}

          />
          <text x={0} dy={data.fontStyle.size * 1.75} fontSize={data.fontStyle.size} fill={'white'} textAnchor='middle'
                pointerEvents={'none'}>
            <textPath href={'#' + id} startOffset={'26.4%'}>
              <tspan fontFamily={'FontAwesome'}>{data.icon + '\u2000'}</tspan>
              <tspan>{data.label}</tspan>
            </textPath>
          </text>
        </g>
      </OverlayTrigger>
    );
  }
}

ArcNode.propTypes = {
  data: PropTypes.object
};

export default ArcNode;
