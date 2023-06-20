import React, {useEffect, useState} from 'react';
import {Button, Nav} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import AwsRunTable from './AWSInstanceTable';
import {faInfoCircle, faSync} from '@fortawesome/free-solid-svg-icons';
import AuthComponent from '../../../AuthComponent';
import InlineSelection from '../../../ui-components/inline-selection/InlineSelection';
import {getAllMachines, getIslandIPsFromMachines} from '../../../utils/ServerUtils';


const AWSRunOptions = (props) => {
  return InlineSelection(getContents, {
    ...props,
    onBackButtonClick: () => {props.setComponent()}
  })
}


const getContents = (props) => {
  let AWSInstances = [{'id': '1', 'instance_id': 'instance_id-1', 'os': 'linux'}, {'instance_id': 'instance_id-2', 'os': 'windows', 'id': '2'}];

  const authComponent = new AuthComponent({});

  let [allIPs, setAllIPs] = useState([]);
  let [selectedIp, setSelectedIp] = useState(null);
  let [AWSClicked, setAWSClicked] = useState(false);
  // eslint-disable-next-line no-unused-vars
  let [runResults, setRunResults] = useState([]);
  let [selectedInstances, setSelectedInstances] = useState([]);

  useEffect(() => {
    getIps();
  }, []);

  function getIps() {
    getAllMachines(true).then(machines => {
        let islandIPs = getIslandIPsFromMachines(machines);
        setAllIPs(islandIPs);
        setSelectedIp(islandIPs[0]);
      });
  }

  function runOnAws() {
    setAWSClicked(true);
    let instances = selectedInstances.map(x => instanceIdToInstance(x));

    authComponent.authFetch('/api/remote-monkey',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: 'aws', instances: instances, island_ip: selectedIp})
      }, true).then(res => res.json())
      .then(res => {
        let result = res['result'];

        // update existing state, not run-over
        let prevRes = result;
        for (let key in result) {
          if (Object.prototype.hasOwnProperty.call(result, key)) {
            prevRes[key] = result[key];
          }
        }
        setRunResults(prevRes);
        setSelectedInstances([]);
        setAWSClicked(false);
      });
  }

  function instanceIdToInstance(instance_id) {
    let instance = props.AWSInstances.find(
      function (inst) {
        return inst['instance_id'] === instance_id;
      });

    return {'instance_id': instance_id, 'os': instance['os']}
  }

  return (
    <div style={{'marginBottom': '2em'}}>
      <div style={{'marginTop': '1em', 'marginBottom': '1em'}}>
        <p className="alert alert-info">
          <FontAwesomeIcon icon={faInfoCircle} style={{'marginRight': '5px'}}/>
          Not sure what this is? Not seeing your AWS EC2 instances? <a
          href="https://techdocs.akamai.com/infection-monkey/docs/running-the-monkey-on-aws-ec2-instances/"
          rel="noopener noreferrer" target="_blank">Read the documentation</a>!
        </p>
      </div>
      {
        allIPs.length > 1 ?
          <Nav variant="pills" activeKey={selectedIp} onSelect={setSelectedIp}
               style={{'marginBottom': '2em'}}>
            {allIPs.map(ip => <Nav.Item key={ip}><Nav.Link eventKey={ip}>{ip}</Nav.Link></Nav.Item>)}
          </Nav>
          : <div style={{'marginBottom': '2em'}}/>
      }
      <AwsRunTable
        data={AWSInstances}
        results={runResults}
        selection={selectedInstances}
        setSelection={setSelectedInstances}
      />
      <div className={'aws-run-button-container'}>
        <Button
          size={'lg'}
          onClick={runOnAws}
          className={'btn btn-default btn-md center-block'}
          disabled={AWSClicked}>
          Run on selected machines
          {AWSClicked ?
            <FontAwesomeIcon icon={faSync} className={`text-success spinning-icon`} style={{'marginLeft': '5px'}}/> : null}
        </Button>
      </div>
    </div>
  );
}

export default AWSRunOptions;
