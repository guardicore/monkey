import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faHandPointLeft} from '@fortawesome/free-solid-svg-icons/faHandPointLeft'
import {
  AgentLogDownloadButton,
  IslandLogDownloadButton
} from '../../ui-components/LogDownloadButtons';
import ExploitionTimeline from './ExploitionTimeline';

const PreviewPaneComponent = (props: any) => {

  function osRow(asset) {
    return (
      <tr>
        <th>Operating System</th>
        <td>{asset.operatingSystem.charAt(0).toUpperCase() + asset.operatingSystem.slice(1)}</td>
      </tr>
    );
  }

  function ipsRow(asset) {
    return (
      <tr>
        <th>IP Addresses</th>
        <td>{asset.networkInterfaces.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  function statusRow(asset) {
    return (
      <tr>
        <th>Status</th>
        <td>{(asset.agentRunning) ? 'Alive' : 'Dead'}</td>
      </tr>
    );
  }

  function logFilename(asset) {
    return asset.agentStartTime.toISOString().split(':').join('.') +
      '-' +
      asset.getLabel().split(/[:/]/).join('-') +
      '.log';
  }

  function downloadLogsRow(asset) {
    return (
      <>
        <tr>
          <th>
            Download Monkey Agent Log
          </th>
          <td>
            <AgentLogDownloadButton url={'/api/agent-logs/' + asset.agentId}
                                    filename={logFilename(asset)}
                                    variant={asset.agentId && !asset.agentRunning ? undefined : 'disabled'}/>
          </td>
        </tr>
        {(asset.island) &&
          <tr>
            <th>
              Download Island Server Log
            </th>
            <td>
              <IslandLogDownloadButton url={'/api/island/log'}/>
            </td>
          </tr>
        }
      </>
    );
  }

  function islandAssetInfo() {
    return (
      <div>
        No info to show
      </div>
    );
  }

  function assetInfo(asset) {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          {osRow(asset)}
          {ipsRow(asset)}
          {downloadLogsRow(asset)}
          </tbody>
        </table>
        <ExploitionTimeline  asset={asset} />
      </div>
    );
  }

  function infectedAssetInfo(asset) {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          {osRow(asset)}
          {statusRow(asset)}
          {ipsRow(asset)}
          {downloadLogsRow(asset)}
          </tbody>
        </table>
        <ExploitionTimeline  asset={asset} />
      </div>
    );
  }

  function edgeInfo() {
    return (
      <div>
      </div>
    );
  }

  let info = null;
  switch (props.type) {
    case 'edge':
      info = edgeInfo();
      break;
    case 'node':
      if (props.item.agentId) {
        info = infectedAssetInfo(props.item)
      } else if (props.item.island) {
        info = islandAssetInfo();
      } else {
        info = assetInfo(props.item)
      }
      break;
  }

  let label = '';
  if (!props.item) {
    label = '';
  } else if ('getLabel' in props.item) {
    label = props.item.getLabel();
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

export default PreviewPaneComponent;
