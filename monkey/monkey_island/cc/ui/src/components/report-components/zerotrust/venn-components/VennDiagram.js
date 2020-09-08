import React from 'react'
import PropTypes from 'prop-types'
import CircularNode from './CircularNode'
import ArcNode from './ArcNode'
import {TypographicUtilities} from './Utility.js'
import './VennDiagram.css'
import {ZeroTrustStatuses} from '../ZeroTrustPillars';

class VennDiagram extends React.Component {
  constructor(props_) {
    super(props_);

    this.state = {hover: true, currentPopover: undefined};
    this._disableHover = this._disableHover.bind(this);

    this.width = this.height = 512;

    this.prefix = 'vennDiagram';
    this.fontStyles = [{size: Math.max(9, this.width / 28), color: 'white'}, {
      size: Math.max(6, this.width / 38),
      color: 'white'
    }, {size: Math.max(6, this.width / 48), color: 'white'}];
    this.offset = this.width / 16;

    this.thirdWidth = this.width / 3;
    this.width11By2 = this.width / 5.5;
    this.width2By7 = 2 * this.width / 7;
    this.width1By11 = this.width / 11;
    this.width1By28 = this.width / 28;
    this.arcNodesGap = 4;

    this.layout = {
      Data: {cx: 0, cy: 0, r: this.width11By2, offset: {x: 0, y: 0}, popover: 'top'},
      People: {
        cx: -this.width2By7,
        cy: 0,
        r: this.width11By2,
        offset: {x: this.width1By11 + this.fontStyles[1].size / 5 * 3, y: 0},
        popover: 'right'
      },
      Networks: {
        cx: this.width2By7,
        cy: 0,
        r: this.width11By2,
        offset: {x: -this.width1By11 - this.fontStyles[1].size / 5 * 3, y: 0},
        popover: 'left'
      },
      Devices: {
        cx: 0,
        cy: this.width2By7,
        r: this.width11By2,
        offset: {x: 0, y: -this.width1By11 + this.fontStyles[1].size / 6 * 3},
        popover: 'top'
      },
      Workloads: {
        cx: 0,
        cy: -this.width2By7,
        r: this.width11By2,
        offset: {x: 0, y: this.width1By11},
        popover: 'bottom'
      },
      VisibilityAndAnalytics: {
        inner: this.thirdWidth - this.width1By28,
        outer: this.thirdWidth,
        icon: '\uf070',
        popover: 'right'
      },
      AutomationAndOrchestration: {
        inner: this.thirdWidth - this.width1By28 * 2 - this.arcNodesGap,
        outer: this.thirdWidth - this.width1By28 - this.arcNodesGap,
        icon: '\uf085',
        popover: 'right'
      }
    };

    /*

    RULE #1: All scores have to be equal 0, except Unexecuted [U] which could be also a negative integer
             sum(C, I, P) has to be <=0

    RULE #2: Failed [C] has to be > 0,
             sum(C) > 0

    RULE #3: Verify [I] has to be > 0 while Failed has to be 0,
             sum(C, I) > 0 and C * I = 0, while C has to be 0

    RULE #4: By process of elimination, passed.
             if the P is bigger by 2 then negative U, first conditional
             would be true.
    */

    this.rules = [

      {
        id: 'Rule #1', status: ZeroTrustStatuses.unexecuted, hex: '#777777', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] + d_[ZeroTrustStatuses.verify] + d_[ZeroTrustStatuses.passed] === 0;
        }
      },
      {
        id: 'Rule #2', status: ZeroTrustStatuses.failed, hex: '#D9534F', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] > 0;
        }
      },
      {
        id: 'Rule #3', status: ZeroTrustStatuses.verify, hex: '#F0AD4E', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] === 0 && d_[ZeroTrustStatuses.verify] > 0;
        }
      },
      {
        id: 'Rule #4', status: ZeroTrustStatuses.passed, hex: '#5CB85C', f: function (d_) {
          return d_[ZeroTrustStatuses.passed] > 0;
        }
      }

    ];

  }

  componentDidMount() {
    this.parseData();
    if (this.state.currentPopover !== undefined) {
      this.state.currentPopover.show();
    }
  }

  _disableHover(ref_) {
    this.setState({hover: false, currentPopover: ref_, data: this.state.data});
  }

  _onMouseMove(e) {

    let self = this;

    if (this.state.currentPopover !== undefined) {
      this.state.currentPopover.show();
    }

    document.querySelectorAll('circle, path').forEach((d_) => {
      d_.setAttribute('opacity', '0.8');
    });

    if (e.target.id.includes('Node')) {

      e.target.setAttribute('opacity', 0.95);

      // Set highest z-index
      e.target.parentNode.parentNode.appendChild(e.target.parentNode);

    } else {

      // Return z indices to default
      Object.keys(this.layout).forEach(function (_d, i_) {
        document.querySelector('#' + self.prefix).appendChild(document.querySelector('#' + self.prefix + 'Node_' + i_).parentNode);
      })
    }

  }

  _onClick(e) {

    if (!e.target.id.includes('Node')) {

      this.state.currentPopover.hide();
      this.setState({hover: true, currentPopover: undefined, data: this.state.data});
    }
  }

  parseData() {

    let self = this;
    let data = [];
    const omit = (prop, {[prop]: _, ...rest}) => rest;

    this.props.pillarsGrades.forEach((d_) => {

      let params = omit('pillar', d_);
      let key = TypographicUtilities.removeAmpersand(d_.pillar);
      let html = self.buildTooltipHtmlContent(params);
      let rule = null;

      for (let j = 0; j < self.rules.length; j++) {
        if (self.rules[j].f(d_)) {
          rule = j;
          break;
        }
      }

      self.setLayoutElement(rule, key, html, d_);
      data.push(this.layout[key]);

    });

    this.setState({hover: true, activePopover: undefined, data: data});
    this.render();
  }

  buildTooltipHtmlContent(object_) {

    return Object.keys(object_).map((key_, i_) => {
      return (<p key={this.prefix + key_ + i_}>{key_}: {object_[key_]}</p>)
    })
  }

  setLayoutElement(rule_, key_, html_, d_) {

    if (rule_ === null) {
      console.log(Error('The node scores are invalid, please check the data or the rules set.'));
    }

    if (key_ === 'Data') {
      this.layout[key_].fontStyle = this.fontStyles[0];
    } else if (Object.prototype.hasOwnProperty.call(this.layout[key_], 'cx')) {
      this.layout[key_].fontStyle = this.fontStyles[1];
    } else {
      this.layout[key_].fontStyle = this.fontStyles[2];
    }

    this.layout[key_].hex = this.rules[rule_].hex;
    this.layout[key_].status = this.rules[rule_].status;
    this.layout[key_].label = d_.pillar;
    this.layout[key_].node = d_;
    this.layout[key_].tooltip = html_;
  }

  render() {
    if (this.state.data === undefined) {
      return null;
    } else {
      // equivalent to center translate (width/2, height/2)
      let viewPortParameters = (-this.width / 2) + ' ' + (-this.height / 2) + ' ' + this.width + ' ' + this.height;
      let nodes = Object.values(this.layout).map((d_, i_) => {
        if (Object.prototype.hasOwnProperty.call(d_, 'cx')) {
          return (
            <CircularNode
              prefix={this.prefix}
              key={this.prefix + 'CircularNode' + i_}
              index={i_}
              data={d_}
              hover={this.state.hover}
              disableHover={this._disableHover}
            />
          );
        } else {
          d_.label = TypographicUtilities.removeBrokenBar(d_.label);
          return (
            <ArcNode
              prefix={this.prefix}
              key={this.prefix + 'ArcNode' + i_}
              index={i_}
              data={d_}
              hover={this.state.hover}
              disableHover={this._disableHover}
            />
          );
        }
      });

      return (
        <div ref={(divElement) => this.divElement = divElement} onMouseMove={this._onMouseMove.bind(this)}
             onClick={this._onClick.bind(this)}>
          <svg id={this.prefix} viewBox={viewPortParameters} width={'100%'} height={'100%'}
               xmlns='http://www.w3.org/2000/svg' xmlnsXlink='http://www.w3.org/1999/xlink'>
            {nodes}
          </svg>
        </div>
      )
    }
  }
}

VennDiagram.propTypes = {
  pillarsGrades: PropTypes.array
};

export default VennDiagram;
