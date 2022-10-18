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
import IslandHttpClient from '../../IslandHttpClient';

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
        <td>{asset.operatingSystem.charAt(0).toUpperCase() + asset.operatingSystem.slice(1)}</td>
      </tr>
    );
  }

  ipsRow(asset) {
    return (
      <tr>
        <th>IP Addresses</th>
        <td>{asset.networkInterfaces.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  statusRow(asset) {
    return (
      <tr>
        <th>Status</th>
        <td>{(asset.agentRunning) ? 'Alive' : 'Dead'}</td>
      </tr>
    );
  }

  logFilename(asset) {
    return asset.agentStartTime.toISOString().split(':').join('.') +
           '-' +
           asset.getLabel().split(/[:/]/).join('-') +
           '.log';
  }

  downloadLogsRow(asset) {
    return (
      <>
        <tr>
          <th>
            Download Monkey Agent Log
          </th>
          <td>
            <AgentLogDownloadButton url={'/api/agent-logs/' + asset.agentId}
              filename={this.logFilename(asset)}
              variant={asset.agentId && ! asset.agentRunning ? undefined : 'disabled'} />
          </td>
        </tr>
        {(asset.island) &&
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
    IslandHttpClient.get("/api/agent-events?type=ExploitationEvent")
      .then(res => res.body)
      .then(events => {
        events.filter(event => asset.ip_addresses.includes(event.target)) // TODO: check values and update when MapNode work is done
      })
      .then(filteredEvents => {
        // TODO: Figure out how to return this; use state?
        if (filteredEvents.length === 0) {
          return (<div/>);
        }
        // TODO: exploitEvent.source is the agent ID, needs to be the IP address
        return (
          <div>
            <h4 style={{'marginTop': '2em'}}>
              Exploit Timeline&nbsp;
              {this.generateToolTip('Timeline of exploit attempts. Red is successful. Gray is unsuccessful')}
            </h4>
            <ul className='timeline'>
              {filteredEvents.map(exploitEvent =>
                <li key={exploitEvent.timestamp}>
                  <div className={'bullet ' + (exploitEvent.success ? 'bad' : '')}/>
                  <div>{new Date(exploitEvent.timestamp).toLocaleString()}</div>
                  <div>{exploitEvent.source}</div>
                  <div>{exploitEvent.exploiter_name}</div>
                </li>
              )}
            </ul>
          </div>
        )
      });
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

  edgeInfo() {
    return (
      <div>
      </div>
    );
  }

  render() {
    let info = null;
    switch (this.props.type) {
      case 'edge':
        info = this.edgeInfo();
        break;
      case 'node':
        if (this.props.item.agentId) {
          info = this.infectedAssetInfo(this.props.item)
        } else if (this.props.item.island) {
          info = this.islandAssetInfo();
        } else {
          info = this.assetInfo(this.props.item)
        }
        break;
    }

    let label = '';
    if (!this.props.item) {
      label = '';
    } else if ('getLabel' in this.props.item) {
      label = this.props.item.getLabel();
    } else {
      label = '';
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
