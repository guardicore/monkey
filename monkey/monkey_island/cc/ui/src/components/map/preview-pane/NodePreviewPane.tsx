import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faHandPointLeft} from '@fortawesome/free-solid-svg-icons/faHandPointLeft'
import {
  AgentLogDownloadButton,
  IslandLogDownloadButton
} from '../../ui-components/LogDownloadButtons';
import ExploitationTimeline from './ExploitationTimeline';
import _ from 'lodash';


const NodePreviewPane = (props: any) => {

  function osRow(node) {
    let os = node.getOperatingSystem();
    return (
      <tr>
        <th>Operating System</th>
        <td>{os.charAt(0).toUpperCase() + os.slice(1)}</td>
      </tr>
    );
  }

  function ipsRow(node) {
    return (
      <tr>
        <th>IP Addresses</th>
        <td>{node.networkInterfaces.map(val => <div key={val}>{val}</div>)}</td>
      </tr>
    );
  }

  function statusRow(node) {
    return (
      <tr>
        <th>Status</th>
        <td>{(node.agentRunning) ? 'Alive' : 'Dead'}</td>
      </tr>
    );
  }



  function downloadLogsRow(node) {
    const agentLogDownloadDisabled = _.isEmpty(node.agentIds) || node.agentRunning;
    return (
      <>
        <tr>
          <th>
            Download Monkey Agent Log
          </th>
          <td>
            <AgentLogDownloadButton url={'/api/agent-logs/'}
                                    agentIds={node.agentIds}
                                    agentsStartTime={node.agentsStartTime}
                                    nodeLabel={node.getLabel()}
                                    disabled={agentLogDownloadDisabled}/>
          </td>
        </tr>
        {(node.island) &&
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
        <table className='table table-condensed'>
          <tbody>
          {osRow(props.item)}
          {props.item.agentId ? statusRow(props.item) : ''}
          {ipsRow(props.item)}
          {downloadLogsRow(props.item)}
          </tbody>
        </table>
      </div>
    );
  }

  function nodeInfo() {
    return (
      <div>
        <table className='table table-condensed'>
          <tbody>
          {osRow(props.item)}
          {props.item.agentId ? statusRow(props.item) : ''}
          {ipsRow(props.item)}
          {downloadLogsRow(props.item)}
          </tbody>
        </table>
        <ExploitationTimeline node={props.item} allNodes={props.allNodes}/>
      </div>
    );
  }

  let info = null;
  switch (props.type) {
    case 'edge':
      info = null;
      break;
    case 'node':
      if (props.item.island) {
        info = islandAssetInfo();
      } else {
        info = nodeInfo();
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
          Select a node on the map for a detailed look
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

export default NodePreviewPane;
