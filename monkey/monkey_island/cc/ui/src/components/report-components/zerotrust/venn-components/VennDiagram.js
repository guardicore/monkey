import React from 'react'
import PropTypes from 'prop-types'
import Tooltip from './Tooltip'
import CircularNode from './CircularNode'
import ArcNode from './ArcNode'
import {TypographicUtilities} from './Utility.js'
import './VennDiagram.css'

class VennDiagram extends React.Component {
  constructor(props_) {
    super(props_);

    this.state = {tooltip: {top: 0, left: 0, display: 'none', html: ''}};

    this.width = this.height = 512;

    this.colors = ['#777777', '#D9534F', '#F0AD4E', '#5CB85C'];
    this.prefix = 'vennDiagram';
    this.suffices = ['', '|tests are|conclusive', '|tests were|inconclusive', '|tests|performed'];
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

    this.toggle = false;

    this.layout = {
      Data: {cx: 0, cy: 0, r: this.thirdWidth - this.offset * 2, offset: {x: 0, y: 0}},
      People: {cx: -this.width2By7, cy: 0, r: this.sixthWidth, offset: {x: this.width1By11, y: 0}},
      Networks: {cx: this.width2By7, cy: 0, r: this.sixthWidth, offset: {x: -this.width1By11, y: 0}},
      Devices: {cx: 0, cy: this.width2By7, r: this.sixthWidth, offset: {x: 0, y: -this.width1By11}},
      Workloads: {cx: 0, cy: -this.width2By7, r: this.sixthWidth, offset: {x: 0, y: this.width1By11}},
      VisibilityAndAnalytics: {inner: this.thirdWidth - this.width1By28, outer: this.thirdWidth},
      AutomationAndOrchestration: {
        inner: this.thirdWidth - this.width1By28 * 2,
        outer: this.thirdWidth - this.width1By28
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
        id: 'Rule #1', f: function (d_) {
          return d_['Conclusive'] + d_['Inconclusive'] + d_['Positive'] === 0;
        }
      },
      {
        id: 'Rule #2', f: function (d_) {
          return d_['Conclusive'] > 0;
        }
      },
      {
        id: 'Rule #3', f: function (d_) {
          return d_['Conclusive'] === 0 && d_['Inconclusive'] > 0;
        }
      },
      {
        id: 'Rule #4', f: function (d_) {
          return d_['Positive'] + d_['Unexecuted'] >= 2 && d_['Positive'] * d_['Unexecuted'] > 0;
        }
      }

    ];

    this._onScroll = this._onScroll.bind(this);
  }

  componentDidMount() {
    this.parseData();
    window.addEventListener('scroll', this._onScroll);
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
        html = e.target.dataset.tooltip;
        this.divElement.style.cursor = 'pointer';
        hidden = 'block';
        e.target.setAttribute('opacity', 0.95);
        bcolor = e.target.getAttribute('fill');

        // Set highest z-index
        e.target.parentNode.parentNode.appendChild(e.target.parentNode);
      } else {
        this.divElement.style.cursor = 'default';

        // Return z indices to default
        Object.keys(this.layout).forEach(function (d_, i_) {
          document.querySelector('#' + self.prefix).appendChild(document.querySelector('#' + self.prefix + 'Node_' + i_).parentNode);
        })
      }

      this.setState({
        target: e,
        tooltip: {
          target: e.target,
          bcolor: bcolor,
          top: e.clientY + 8,
          left: e.clientX + 8,
          display: hidden,
          html: html
        }
      });
    }
  }

  _onScroll(e) {
    this.divElement.style.cursor = 'default';
    this.setState({target: null, tooltip: {target: null, bcolor: 'none', top: 0, left: 0, display: 'none', html: ''}});
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
      let sum = Object.keys(params).reduce((sum_, key_) => sum_ + parseFloat(params[key_] || 0), 0);
      let key = TypographicUtilities.removeAmpersand(d_.pillar);
      let html = self.buildTooltipHtmlContent(d_);
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
    return Object.keys(object_).reduce((out_, key_) => out_ + TypographicUtilities.setTitle(key_) + ': ' + object_[key_] + '\n', '');
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

    this.layout[key_].hex = this.colors[rule_];
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
          <Tooltip id={this.prefix + 'Tooltip'} prefix={this.prefix} {...this.state.tooltip} />
        </div>
      )
    }
  }
}

VennDiagram.propTypes = {
  pillarsGrades: PropTypes.array
};

export default VennDiagram;
