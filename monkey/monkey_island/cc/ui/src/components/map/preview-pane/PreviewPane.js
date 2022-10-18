import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faHandPointLeft} from '@fortawesome/free-solid-svg-icons/faHandPointLeft'
import {faQuestionCircle} from '@fortawesome/free-solid-svg-icons/faQuestionCircle'
import {OverlayTrigger, Tooltip} from 'react-bootstrap';
import AuthComponent from '../../AuthComponent';
import {
  AgentLogDownloadButton,
  IslandLogDownloadButton
} from '../../ui-components/LogDownloadButtons';

class PreviewPaneComponent extends AuthComponent {

  generateToolTip(text) {
    return (
      <OverlayTrigger placement="top"
                      overlay={<Tooltip id="tooltip">{text}</Tooltip>}
                      delay={{show: 250, hide: 400}}>
        <a><FontAwesomeIcon icon={faQuestionCircle} style={{'marginRight': '0.5em'}}/></a>
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

  statusRow(asset) {
    return (
      <tr>
        <th>Status</th>
        <td>{(asset.dead) ? 'Dead' : 'Alive'}</td>
      </tr>
    );
  }

  downloadLogsRow(asset) {
    return (
      <>
        <tr>
          <th>
            Download Monkey Agent Log
          </th>
          <td>
            <AgentLogDownloadButton url={'/api/log?id=' + asset.id}
                               variant={asset.has_log ? undefined : 'disabled'}/>
          </td>
        </tr>
        {(asset['group'].includes('island')) &&
          <tr>
            <th>
              Download Island Server Log
            </th>
            <td>
              <IslandLogDownloadButton url={'/api/island/log'} />
            </td>
          </tr>
        }
      </>
    );
  }


  exploitsTimeline(asset) {
    if (asset.exploits.length === 0) {
      return (<div/>);
    }
    return (
      <div>
        <h4 style={{'marginTop': '2em'}}>
          Exploit Timeline&nbsp;
          {this.generateToolTip('Timeline of exploit attempts. Red is successful. Gray is unsuccessful')}
        </h4>
        <ul className='timeline'>
          {asset.exploits.map(exploit =>
            <li key={exploit.timestamp}>
              <div className={'bullet ' + (exploit.exploitation_result ? 'bad' : '')}/>
              <div>{new Date(exploit.timestamp).toLocaleString()}</div>
              <div>{exploit.origin}</div>
              <div>{exploit.exploiter}</div>
            </li>
          )}
        </ul>
      </div>
    )
  }

  islandAssetInfo() {
    return (
      <div>
        No info to show
      </div>
    );
  }

  assetInfo(asset) {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          {this.osRow(asset)}
          {this.ipsRow(asset)}
          {this.downloadLogsRow(asset)}
          </tbody>
        </table>
        {this.exploitsTimeline(asset)}
      </div>
    );
  }

  infectedAssetInfo(asset) {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          {this.osRow(asset)}
          {this.statusRow(asset)}
          {this.ipsRow(asset)}
          {this.downloadLogsRow(asset)}
          </tbody>
        </table>
        {this.exploitsTimeline(asset)}
      </div>
    );
  }

  scanInfo(edge) {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          <tr>
            <th>Operating System</th>
            <td>{edge.os.type}</td>
          </tr>
          <tr>
            <th>IP Address</th>
            <td>{edge.ip_address}</td>
          </tr>
          </tbody>
        </table>
        {
          (edge.exploits.length === 0) ?
            '' :
            <div>
              <h4 style={{'marginTop': '2em'}}>Timeline</h4>
              <ul className='timeline'>
                {edge.exploits.map(exploit =>
                  <li key={exploit.timestamp}>
                    <div className={'bullet ' + (exploit.result ? 'bad' : '')}/>
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
        if (this.props.item.group.includes('monkey')) {
          info = this.assetInfo(this.props.item);
        } else if (this.props.item.group.includes('monkey', 'manual')) {
          info = this.infectedAssetInfo(this.props.item)
        } else if (this.props.item.group !== 'island') {
          info = this.assetInfo(this.props.item)
        } else {
          info = this.islandAssetInfo();
        }
        break;
      case 'island_edge':
        info = this.islandEdgeInfo();
        break;
    }

    let label = '';
    if (!this.props.item) {
      label = '';
    } else if (Object.prototype.hasOwnProperty.call(this.props.item, 'label')) {
      label = this.props.item['label'];
    } else if (Object.prototype.hasOwnProperty.call(this.props.item, '_label')) {
      label = this.props.item['_label'];
    }

    return (
      <div className='preview-pane'>
        {!info ?
          <span>
            <FontAwesomeIcon icon={faHandPointLeft} style={{'marginRight': '0.5em'}}/>
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
