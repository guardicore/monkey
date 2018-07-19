import React from 'react';
import {Icon} from 'react-fa';
import Toggle from 'react-toggle';
import {OverlayTrigger, Tooltip} from 'react-bootstrap';
import download from 'downloadjs'
import PreviewPaneComponent from 'components/map/preview-pane/PreviewPane';

class PthPreviewPaneComponent extends PreviewPaneComponent {
  nodeInfo(asset) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          <tr>
            <th>Hostname</th>
            <td>{asset.hostname}</td>
          </tr>
          <tr>
            <th>IP Addresses</th>
            <td>{asset.ips.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          <tr>
            <th>Services</th>
            <td>{asset.services.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          <tr>
            <th>Compromised Users</th>
            <td>{asset.users.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          </tbody>
        </table>
      </div>
    );
  }

  edgeInfo(edge) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          <tr>
            <th>Compromised Users</th>
            <td>{edge.users.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          </tbody>
        </table>
      </div>
    );
  }

  getInfoByProps() {
    switch (this.props.type) {
      case 'edge':
        return this.edgeInfo(this.props.item);
      case 'node':
        return this.nodeInfo(this.props.item);
    }

    return null;
  }
}

export default PthPreviewPaneComponent;
