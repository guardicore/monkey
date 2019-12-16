import React from 'react'
import PillarLabel from '../PillarLabel';
import {Popover, OverlayTrigger} from 'react-bootstrap';
import PropTypes from 'prop-types';

class CircularNode extends React.Component {
  render() {
    let {prefix, index, data} = this.props;

    let translate = 'translate(' + data.cx + ',' + data.cy + ')';
    return (
      <g transform={translate} id={data.node.pillar} key={prefix + 'circularGroup' + index}>
        <OverlayTrigger ref={'overlay'} key={prefix + 'CircularOverlay' + index} trigger={null} placement={data.popover}
                        overlay={<Popover id={prefix + 'CircularClickPopover' + index}
                                          style={{backgroundColor: data.hex}}
                                          title={data.node.pillar}>{data.tooltip}</Popover>} rootClose>
          <circle
            id={prefix + 'Node_' + index}
            className={'circularNode'}
            data-tooltip={data.tooltip}
            r={data.r}
            opacity={0.8}
            fill={data.hex}
            onClick={this.handleClick.bind(this)}
            onMouseEnter={this.handleOver.bind(this)}
            onMouseLeave={this.handleOut.bind(this)}

          />
        </OverlayTrigger>
        <foreignObject style={{fontSize: data.fontStyle.size, pointerEvents: 'none'}}
                       key={prefix + 'PillarLabelOject' + index} x={data.offset.x - data.fontStyle.size * 6}
                       y={data.offset.y - data.fontStyle.size} width={data.fontStyle.size * 12}
                       height={data.fontStyle.size * 6}>
          <PillarLabel key={prefix + 'PillarLabel' + index} pillar={data.node.pillar} status={data.status}/>
        </foreignObject>
      </g>
    );
  }


  handleClick() {
    this.props.disableHover(this.refs.overlay);
  }

  handleOver() {
    if (this.props.hover) {
      this.refs.overlay.show();
    }
  }

  handleOut() {
    if (this.props.hover) {
      this.refs.overlay.hide();
    }
  }

}

CircularNode.propTypes = {
  index: PropTypes.number,
  data: PropTypes.object
};

export default CircularNode;
