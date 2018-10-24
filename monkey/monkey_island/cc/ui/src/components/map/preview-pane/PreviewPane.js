import React from 'react';
import {Icon} from 'react-fa';
import Toggle from 'react-toggle';
import {Button, OverlayTrigger, Panel, PanelGroup, Tooltip} from 'react-bootstrap';
import download from 'downloadjs'
import AuthComponent from '../../AuthComponent';
import CollapsedTable from "./CollapsedTable";

class PreviewPaneComponent extends AuthComponent {

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
    this.authFetch('/api/monkey/' + asset.guid,
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
                  onChange={(e) => this.forceKill(e, asset)}/>

        </td>
      </tr>
    );
  }

  unescapeLog(st) {
    return st.substr(1, st.length - 2) // remove quotation marks on beginning and end of string.
        .replace(/\\n/g, "\n")
        .replace(/\\r/g, "\r")
        .replace(/\\t/g, "\t")
        .replace(/\\b/g, "\b")
        .replace(/\\f/g, "\f")
        .replace(/\\"/g, '\"')
        .replace(/\\'/g, "\'")
        .replace(/\\&/g, "\&");
  }

  downloadLog(asset) {
    this.authFetch('/api/log?id=' + asset.id)
      .then(res => res.json())
      .then(res => {
        let timestamp = res['timestamp'];
        timestamp = timestamp.substr(0, timestamp.indexOf('.'));
        let filename = res['monkey_label'].split(':').join('-') + ' - ' + timestamp + '.log';
        let logContent = this.unescapeLog(res['log']);
        download(logContent, filename, 'text/plain');
      });

  }

  downloadLogRow(asset) {
    return (
      <tr>
        <th>
          Download Log
        </th>
        <td>
          <a type="button" className="btn btn-primary"
             disabled={!asset.has_log}
             onClick={() => this.downloadLog(asset)}>Download</a>
        </td>
      </tr>
    );
  }

  k8sContainerRow(container) {
    return [
      <tr key={container.name + "-container-name"}>
        <th>Name</th>
        <td>{container.name}</td>
      </tr>,
      <tr key={container.name + "-container-ports"}>
        <th>Ports</th>
        <td>{container.ports.length > 0 ? container.ports.reduce((total, new_str) => total + ', ' + new_str) : 'None'}</td>
      </tr>

    ];
  }

  k8sContainerPanel(k8s_pod) {
    return (
      <PanelGroup accordion id={k8s_pod.name + '-container-panel'}>
        <Panel eventKey="container-panel">
          <Panel.Heading>
            <Panel.Title toggle><b>Pod's Containers</b></Panel.Title>
          </Panel.Heading>
          <Panel.Body collapsible>
            <table className="table table-condensed"><tbody>
            {k8s_pod.containers.map(x => this.k8sContainerRow(x))}
            </tbody></table>
          </Panel.Body>
        </Panel>
      </PanelGroup>
    );
  }

  k8sLabelPanel(k8s_pod) {
    return (
      <PanelGroup accordion id={k8s_pod.name + '-label-panel'}>
        <Panel eventKey="label-panel">
          <Panel.Heading>
            <Panel.Title toggle><b>Pod's Labels</b></Panel.Title>
          </Panel.Heading>
          <Panel.Body collapsible>
            <table className="table table-condensed"><tbody>
            {k8s_pod.labels.map(x => <tr key={x.key}><th>{x.key}</th><td>{x.value}</td></tr>)}
            </tbody></table>
          </Panel.Body>
        </Panel>
      </PanelGroup>
    );
  }

  k8sPodRowsImp(k8s_pod) {
    return [
      <tr key="pod-name">
        <th>Pod Name</th>
        <td>{k8s_pod.name}</td>
      </tr>,
      <tr key="pod-namespace">
        <th>Pod Namespace</th>
        <td>{k8s_pod.namespace}</td>
      </tr>,
      <tr key="pod-host">
        <th>Pod's Host</th>
        <td>{k8s_pod.node_name}</td>
      </tr>,
      <tr key="pod-containers">
        <th/>
        <td>
          {this.k8sContainerPanel(k8s_pod)}
        </td>
      </tr>,
      <tr key="pod-label">
        <th/>
        <td>
          {this.k8sLabelPanel(k8s_pod)}
        </td>
      </tr>
    ];
  }

  k8sPodIpsPanel(pod_ips) {
    return (
      <PanelGroup accordion id={pod_ips.join('-') + '-pod-ips'}>
        <Panel eventKey="container-panel">
          <Panel.Heading>
            <Panel.Title toggle><b>Pods' IPs</b></Panel.Title>
          </Panel.Heading>
          <Panel.Body collapsible>
            <table className="table"><tbody>
            {pod_ips.map(x => <tr key={x}><th/><td>{x}</td></tr>)}
            </tbody></table>
          </Panel.Body>
        </Panel>
      </PanelGroup>
    );
  }

  k8sHostNetworkPodsPanel(asset) {
    let k8s_host_pods = asset.k8s_host_pods;
    return (
      <PanelGroup accordion id={asset.host_ip + "-host-pods"}>
        <Panel eventKey="container-panel">
          <Panel.Heading>
            <Panel.Title toggle><b>Host Network Pods</b></Panel.Title>
          </Panel.Heading>
          <Panel.Body collapsible>
            <table className="table table-condensed"><tbody>
            {k8s_host_pods.map(x => this.k8sPodRowsImp(x))}
            </tbody></table>
          </Panel.Body>
        </Panel>
      </PanelGroup>
    );
  }

  k8sNodeRows(asset) {
    return [
      <tr key="k8s-node">
        <th>Kubernetes</th>
        <td>Node</td>
      </tr>,
      <tr key="node-name">
        <th>Node Name</th>
        <td>{asset.k8s_node.name}</td>
      </tr>,
      <tr key="pod-ips-label">
        Pods' IP Addresses
      </tr>,
      <tr key="pods-ips">
          {this.k8sPodIpsPanel(asset.k8s_node.pod_ips)}
      </tr>,
      <tr key="host-network-pods">
        <th/>
        <td>
          {this.k8sHostNetworkPodsPanel(asset)}
        </td>
      </tr>
    ];
  }

  k8sPodRows(asset) {
    return [
      <tr key="k8s-pod">
        <th>Kubernetes</th>
        <td>Pod</td>
      </tr>
    ].concat(this.k8sPodRowsImp(asset.k8s_pod));
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
        <ul className="timeline">
          {asset.exploits.map(exploit =>
            <li key={exploit.timestamp}>
              <div className={'bullet ' + (exploit.result ? 'bad' : '')}/>
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

  assetInfo(asset, isInfected) {
    let isK8sPod = asset.hasOwnProperty('k8s_pod');
    let isK8sNode = asset.hasOwnProperty('k8s_node');
    return (
      <div>
        <table className="table table-condensed">
          <tbody>
          {this.osRow(asset)}
          {isInfected ? this.statusRow(asset) : undefined}
          {this.ipsRow(asset)}
          {this.servicesRow(asset)}
          {this.accessibleRow(asset)}
          {isInfected ? this.forceKillRow(asset) : undefined}
          {isInfected ? this.downloadLogRow(asset) : undefined}
          </tbody>
        </table>
        <table className="table table-condensed">
          <tbody>
          {this.osRow(asset)}
          {isK8sNode ? this.k8sNodeRows(asset) : isK8sPod ? this.k8sPodRows(asset) : undefined}
          </tbody>
        </table>
        <hr/>
        <h4>
          <b>Pods' IPs</b>
        </h4>
        <div>
          {isK8sNode ?
            <CollapsedTable
              parseItemFunction={x => <tr key={x}><th/><td>{x}</td></tr>}
              tableItems={asset.k8s_node.pod_ips}
            />
            :
            undefined
          }
        </div>
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
        if (this.props.item.group !== 'host') {
          info = this.scanInfo(this.props.item);
        }
        break;
      case 'node':
        info = this.props.item.group.includes('monkey', 'manual') ? this.assetInfo(this.props.item, true) :
          this.props.item.group !== 'island' ? this.assetInfo(this.props.item, false) : this.islandAssetInfo();
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
