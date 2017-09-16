import React from 'react';
import {Icon} from "react-fa";

class PreviewPaneComponent extends React.Component {
  assetInfo(asset) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          <tr>
            <th>Operating System</th>
            <td>{asset.os}</td>
          </tr>
          <tr>
            <th>IP Addresses</th>
            <td>{asset.ip_addresses.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          <tr>
            <th>Services</th>
            <td>{asset.services.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          <tr>
            <th>Accessible From</th>
            <td>{asset.accessible_from_nodes.map(val => <div key={val.id}>{val.id}</div>)}</td>
          </tr>
          </tbody>
        </table>
      </div>
    );
  }

  infectedAssetInfo(asset) {
    return (
      <div>
        {this.assetInfo(asset)}

        <h4 style={{'marginTop': '2em'}}>Timeline</h4>
        <ul className="timeline">
          { asset.exploits.map(exploit =>
            <li key={exploit.start_timestamp}>
              <div className={'bullet ' + (exploit.result ? 'bad' : '')}></div>
              <div>{exploit.start_timestamp}</div>
              <div>{exploit.origin}</div>
              <div>{exploit.exploiter}</div>
            </li>
          )}
        </ul>
      </div>
    );
  }

  infectionInfo(edge) {
    return (
      <div>

      </div>
    );
  }

  scanInfo(edge) {
    return (
      <div>

      </div>
    );
  }

  render() {
    let info = null;
    switch (this.props.type) {
      case 'edge':
        info = this.props.item.exploits.length ?
          this.infectionInfo(this.props.item) : this.scanInfo(this.props.item);
      case 'node':
        info = this.props.item.exploits.some(exploit => exploit.result) ?
          this.infectedAssetInfo(this.props.item) : this.assetInfo(this.props.item);
    }
    return (
      <div className="preview-pane">
        { !this.props.item ?
          <span>
            <Icon name="hand-o-left" style={{'marginRight': '0.5em'}}></Icon>
            Select an item on the map for a preview
          </span>
        :
          <div>
            <h3>
              <b>{this.props.item.label}</b>
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
