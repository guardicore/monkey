import React from 'react';
import {Icon} from 'react-fa';
import Toggle from 'react-toggle';
import {OverlayTrigger, Tooltip} from 'react-bootstrap';

class PreviewPaneComponent extends React.Component {

  generateToolTip(text) {
    return (
      <OverlayTrigger placement="top" overlay={<Tooltip id="tooltip">{text}</Tooltip>}>
        <a><i className="glyphicon glyphicon-info-sign"/></a>
      </OverlayTrigger>
    );
  }

  osRow(asset) {
    return (
      <tr>
        <th>Operating System</th>
        <td>{asset.os.charAt(0).toUpperCase() + asset.os.slice(1)}</td>
      </tr>
    );
  }

  ipsRow(asset) {
    return (
      <tr>
        <th>IP Addresses</th>
        <td>{asset.ip_addresses.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  servicesRow(asset) {
    return (
      <tr>
        <th>Services</th>
        <td>{asset.services.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  accessibleRow(asset) {
    return (
      <tr>
        <th>
          Accessible From&nbsp;
          {this.generateToolTip('List of machine which can access this one using a network protocol')}
        </th>
        <td>{asset.accessible_from_nodes.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  statusRow(asset) {
    return (
      <tr>
        <th>Status</th>
        <td>{(asset.dead) ? 'Dead' : 'Alive'}</td>
      </tr>
    );
  }

  forceKill(event, asset) {
    let newConfig = asset.config;
    newConfig['alive'] = !event.target.checked;
    fetch('/api/monkey/' + asset.guid,
      {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({config: newConfig})
      });
  }

  forceKillRow(asset) {
    return (
      <tr>
        <th>
          Force Kill&nbsp;
          {this.generateToolTip('If this is on, monkey will die next time it communicates')}
        </th>
        <td>
          <Toggle id={asset.id} checked={!asset.config.alive} icons={false} disabled={asset.dead}
                  onChange={(e) => this.forceKill(e, asset)} />

        </td>
      </tr>
    );
  }

  exploitsTimeline(asset) {
    if (asset.exploits.length === 0) {
      return (<div />);
    }

    return (
      <div>
        <h4 style={{'marginTop': '2em'}}>
          Exploit Timeline&nbsp;
          {this.generateToolTip('Timeline of exploit attempts. Red is successful. Gray is unsuccessful')}
        </h4>
        <ul className="timeline">
          { asset.exploits.map(exploit =>
            <li key={exploit.timestamp}>
              <div className={'bullet ' + (exploit.result ? 'bad' : '')} />
              <div>{new Date(exploit.timestamp).toLocaleString()}</div>
              <div>{exploit.origin}</div>
              <div>{exploit.exploiter}</div>
            </li>
          )}
        </ul>
      </div>
    )
  }

  assetInfo(asset) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
            {this.osRow(asset)}
            {this.ipsRow(asset)}
            {this.servicesRow(asset)}
            {this.accessibleRow(asset)}
          </tbody>
        </table>
        {this.exploitsTimeline(asset)}
      </div>
    );
  }

  infectedAssetInfo(asset) {
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
            {this.osRow(asset)}
            {this.statusRow(asset)}
            {this.ipsRow(asset)}
            {this.servicesRow(asset)}
            {this.accessibleRow(asset)}
            {this.forceKillRow(asset)}
          </tbody>
        </table>
        {this.exploitsTimeline(asset)}
      </div>
    );
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
        {
          (edge.exploits.length === 0) ?
            '' :
            <div>
              <h4 style={{'marginTop': '2em'}}>Timeline</h4>
              <ul className="timeline">
                { edge.exploits.map(exploit =>
                  <li key={exploit.timestamp}>
                    <div className={'bullet ' + (exploit.result ? 'bad' : '')} />
                    <div>{new Date(exploit.timestamp).toLocaleString()}</div>
                    <div>{exploit.origin}</div>
                    <div>{exploit.exploiter}</div>
                  </li>
                )}
              </ul>
            </div>
        }
      </div>
    );
  }

  islandEdgeInfo() {
    return (
      <div>
      </div>
    );
  }

  render() {
    let info = null;
    switch (this.props.type) {
      case 'edge':
        info = this.scanInfo(this.props.item);
        break;
      case 'node':
        info = this.props.item.group.includes('monkey', 'manual') ?
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
            <Icon name="hand-o-left" style={{'marginRight': '0.5em'}} />
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
