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
    // TODO: Have exploit info expandable (show detailed attempts)
    // TODO: consider showing scans with exploits on same timeline
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
    return this.scanInfo(edge);
  }

  scanInfo(edge) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          <tr>
            <th>Operating System</th>
            <td>{edge.os.type}</td>
          </tr>
          <tr>
            <th>IP Address</th>
            <td>{edge.ip_address}</td>
          </tr>
          <tr>
            <th>Services</th>
            <td>{edge.services.map(val => <div key={val}>{val}</div>)}</td>
          </tr>
          </tbody>
        </table>
        <h4 style={{'marginTop': '2em'}}>Timeline</h4>
        <ul className="timeline">
          { edge.exploits.map(exploit =>
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

  islandEdgeInfo() {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          <tr>
            <th>Communicates directly with island</th>
            <td>True</td>
          </tr>
          </tbody>
        </table>
      </div>
    );
  }

  render() {
    let info = null;
    switch (this.props.type) {
      case 'edge':
        info = this.props.item.exploits.length ?
          this.infectionInfo(this.props.item) : this.scanInfo(this.props.item);
        break;
      case 'node':
        info = this.props.item.exploits.some(exploit => exploit.result) ?
          this.infectedAssetInfo(this.props.item) : this.assetInfo(this.props.item);
        break;
      case 'island_edge':
      info = this.islandEdgeInfo();
      break;
    }

    let label = '';
    if (!this.props.item) {
      label = '';
    } else if (this.props.item.hasOwnProperty('label')) {
      label = this.props.item['label'];
    } else if (this.props.item.hasOwnProperty('_label')) {
      label = this.props.item['_label'];
    }

    return (
      <div className="preview-pane">
        { !info ?
          <span>
            <Icon name="hand-o-left" style={{'marginRight': '0.5em'}}></Icon>
            Select an item on the map for a preview
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
