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
      <g transform={'rotate(180)'} id={data.node.pillar} key={prefix + 'arcGroup' + index}>
        <OverlayTrigger ref={'overlay'} key={prefix + 'arcOverlayTrigger' + index} trigger={null}
                        placement={data.popover}
                        overlay={<Popover id={prefix + 'ArcPopover' + index} style={{backgroundColor: data.hex}}
                                          title={data.node.pillar}>{data.tooltip}</Popover>} rootClose>
          <path

            id={prefix + 'Node_' + index}
            className={'arcNode'}
            data-tooltip={data.tooltip}
            d={arc()}
            fill={data.hex}
            onClick={this.handleClick.bind(this)}
            onMouseEnter={this.handleOver.bind(this)}
            onMouseLeave={this.handleOut.bind(this)}

          />
        </OverlayTrigger>
        <text x={0} dy={data.fontStyle.size * 1.2} fontSize={data.fontStyle.size} fill={'white'} textAnchor='middle'
              pointerEvents={'none'}>
          <textPath href={'#' + id} startOffset={'26.4%'}>
            <tspan fontFamily={'FontAwesome'}>{data.icon + '\u2000'}</tspan>
            <tspan>{data.label}</tspan>
          </textPath>
        </text>
      </g>
    );
  }


  handleClick(e_) {
    this.props.disableHover(this.refs.overlay);
  }

  handleOver(e_) {
    if (this.props.hover) {
      this.refs.overlay.show();
    }
  }

  handleOut(e_) {
    if (this.props.hover) {
      this.refs.overlay.hide();
    }
  }
}

ArcNode.propTypes = {
  data: PropTypes.object
};

export default ArcNode;
