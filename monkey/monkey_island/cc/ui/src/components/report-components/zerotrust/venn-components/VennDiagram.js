import React from 'react'
import PropTypes from 'prop-types'
import CircularNode from './CircularNode'
import ArcNode from './ArcNode'
import {TypographicUtilities} from './Utility.js'
import './VennDiagram.css'
import {ZeroTrustStatuses} from "../ZeroTrustPillars";

class VennDiagram extends React.Component {
  constructor(props_) {
    super(props_);

    this.state = {tooltip: {top: 0, left: 0, display: 'none', html: ''}};

    this.width = this.height = 512;

    this.prefix = 'vennDiagram';
    this.suffices = ['', '|tests are|failed', '|tests were|inconclusive', '|tests|performed'];
    this.fontStyles = [{size: Math.max(9, this.width / 32), color: 'white'}, {
      size: Math.max(6, this.width / 52),
      color: 'black'
    }];
    this.offset = this.width / 16;

    this.thirdWidth = this.width / 3;
    this.sixthWidth = this.width / 6;
    this.width2By7 = 2 * this.width / 7;
    this.width1By11 = this.width / 11;
    this.width1By28 = this.width / 28;
    this.arcNodesGap = 4;

    this.toggle = false;

    this.layout = {
      Data: {cx: 0, cy: 0, r: this.sixthWidth, offset: {x: 0, y: 0}, popover: 'top'},
      People: {cx: -this.width2By7, cy: 0, r: this.sixthWidth, offset: {x: this.width1By11, y: 0}, popover: 'right'},
      Networks: {cx: this.width2By7, cy: 0, r: this.sixthWidth, offset: {x: -this.width1By11, y: 0}, popover: 'left'},
      Devices: {cx: 0, cy: this.width2By7, r: this.sixthWidth, offset: {x: 0, y: -this.width1By11}, popover: 'top'},
      Workloads: {cx: 0, cy: -this.width2By7, r: this.sixthWidth, offset: {x: 0, y: this.width1By11}, popover: 'bottom'},
      VisibilityAndAnalytics: {inner: this.thirdWidth - this.width1By28, outer: this.thirdWidth, popover: 'right'},
      AutomationAndOrchestration: {
        inner: this.thirdWidth - this.width1By28 * 2 - this.arcNodesGap,
        outer: this.thirdWidth - this.width1By28 - this.arcNodesGap,
        popover: 'right'
      }
    };

    /*

    RULE #1: All scores have to be equal 0, except Unexecuted [U] which could be also a negative integer
             sum(C, I, P) has to be <=0

    RULE #2: Conclusive [C] has to be > 0,
             sum(C) > 0

    RULE #3: Inconclusive [I] has to be > 0 while Conclusive has to be 0,
             sum(C, I) > 0 and C * I = 0, while C has to be 0

    RULE #4: Positive [P] and Unexecuted have to be positive
             sum(P, U) >= 2 and P * U = positive integer, while
             if the P is bigger by 2 then negative U, first conditional
             would be true.

    */

    this.rules = [

      {
        id: 'Rule #1', status: ZeroTrustStatuses.unexecuted, hex: '#777777', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] + d_[ZeroTrustStatuses.inconclusive] + d_[ZeroTrustStatuses.passed] === 0;
        }
      },
      {
        id: 'Rule #2', status: ZeroTrustStatuses.failed, hex: '#D9534F', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] > 0;
        }
      },
      {
        id: 'Rule #3', status: 'Inconclusive', hex: '#F0AD4E', f: function (d_) {
          return d_[ZeroTrustStatuses.failed] === 0 && d_['Inconclusive'] > 0;
        }
      },
      {
        id: 'Rule #4', status: ZeroTrustStatuses.passed, hex: '#5CB85C', f: function (d_) {
          return d_[ZeroTrustStatuses.passed] + d_[ZeroTrustStatuses.unexecuted] >= 2 && d_[ZeroTrustStatuses.passed] * d_[ZeroTrustStatuses.unexecuted] > 0;
        }
      }

    ];

  }

  componentDidMount() {
    this.parseData();
  }

  _onMouseMove(e) {

    let self = this;

    if (!this.toggle) {
      let hidden = 'none';
      let html = '';
      let bcolor = '#DEDEDE';

      document.querySelectorAll('circle, path').forEach((d_, i_) => {
        d_.setAttribute('opacity', "0.8");
      });

      if (e.target.id.includes('Node')) {

        e.target.setAttribute('opacity', 0.95);

        // Set highest z-index
        e.target.parentNode.parentNode.appendChild(e.target.parentNode);
      } else {

        // Return z indices to default
        Object.keys(this.layout).forEach(function (d_, i_) {
          document.querySelector('#' + self.prefix).appendChild(document.querySelector('#' + self.prefix + 'Node_' + i_).parentNode);
        })
      }

    }
  }

  _onClick(e) {
    this.toggle = this.state.tooltip.target === e.target;

    //variable to external callback
    //e.target.parentNode.id)
  }

  parseData() {

    let self = this;
    let data = [];
    const omit = (prop, {[prop]: _, ...rest}) => rest;

    this.props.pillarsGrades.forEach((d_, i_) => {

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

    this.setState({data: data});
    this.render();
  }

  buildTooltipHtmlContent(object_) {

    var out = [];
    Object.keys(object_).forEach(function (d_) {
      out.push([d_ + ': ' + object_[d_], <br/>]);
    });
    return out;

  }

  setLayoutElement(rule_, key_, html_, d_) {
    if (rule_ == null) {
      throw Error('The node scores are invalid');
    }

    if (key_ === 'Data') {
      this.layout[key_].fontStyle = this.fontStyles[0];
    } else {
      this.layout[key_].fontStyle = this.fontStyles[1];
    }

    this.layout[key_].hex = this.rules[rule_].hex;
    this.layout[key_].status = this.rules[rule_].status;
    this.layout[key_].label = d_.pillar + this.suffices[rule_];
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
        if (d_.hasOwnProperty('cx')) {
          return (
            <CircularNode
              prefix={this.prefix}
              key={this.prefix + 'CircularNode' + i_}
              index={i_}
              data={d_}
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
