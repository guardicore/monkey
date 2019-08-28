import React from 'react'
import PillarLabel from "../PillarLabel";
import {Popover, OverlayTrigger} from 'react-bootstrap';
import PropTypes from 'prop-types';

class CircularNode extends React.Component {
  render() {
    let {prefix, index, data} = this.props;

    let translate = 'translate(' + data.cx + ',' + data.cy + ')';
    return (
      <OverlayTrigger key={prefix + 'CircularOverlayTrigger' + index} trigger={['hover', 'focus']}
                      placement={data.popover}
                      overlay={<Popover key={prefix + 'CircularTooltip' + index} id={prefix + 'Popover'}
                                        style={{backgroundColor: data.hex}}
                                        title={data.node.pillar}>{data.tooltip}</Popover>}>
        <g transform={translate} id={data.node.pillar}>
          <circle
            id={prefix + 'Node_' + index}
            className={'circularNode'}
            data-tooltip={data.tooltip}
            r={data.r}
            opacity={0.8}
            fill={data.hex}
          />
          <foreignObject style={{fontSize: data.fontStyle.size, pointerEvents: 'none'}}
                         key={prefix + 'PillarLabel' + index} x={data.offset.x - data.fontStyle.size * 6}
                         y={data.offset.y - data.fontStyle.size} width={data.fontStyle.size * 12}
                         height={data.fontStyle.size * 6}>
            <PillarLabel pillar={data.node.pillar} status={data.status}/>
          </foreignObject>
        </g>
      </OverlayTrigger>
    );
  }
}

CircularNode.propTypes = {
  index: PropTypes.number,
  data: PropTypes.object
};

export default CircularNode;
