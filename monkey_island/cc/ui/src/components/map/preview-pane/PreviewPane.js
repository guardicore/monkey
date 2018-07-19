import React from 'react';
import {Icon} from 'react-fa';
import Toggle from 'react-toggle';
import {OverlayTrigger, Tooltip} from 'react-bootstrap';
import download from 'downloadjs'
import AuthComponent from '../../AuthComponent';

class PreviewPaneComponent extends AuthComponent {

  generateToolTip(text) {
    return (
      <OverlayTrigger placement="top" overlay={<Tooltip id="tooltip">{text}</Tooltip>}>
        <a><i className="glyphicon glyphicon-info-sign"/></a>
      </OverlayTrigger>
    );
  }

  // This should be overridden
  getInfoByProps() {
    return null;
  }

  getLabelByProps() {
    if (!this.props.item) {
      return '';
    } else if (this.props.item.hasOwnProperty('label')) {
      return this.props.item['label'];
    } else if (this.props.item.hasOwnProperty('_label')) {
      return this.props.item['_label'];
    }
    return '';
  }

  render() {
    let info = this.getInfoByProps();
    let label = this.getLabelByProps();

    return (
      <div className="preview-pane">
        {!info ?
          <span>
            <Icon name="hand-o-left" style={{'marginRight': '0.5em'}}/>
            Select an item on the map for a detailed look
          </span>
          :
          <div>
            <h3>
              {label}
            </h3>

            <hr/>
            {info}
          </div>
        }
      </div>
    );
  }
}

export default PreviewPaneComponent;
