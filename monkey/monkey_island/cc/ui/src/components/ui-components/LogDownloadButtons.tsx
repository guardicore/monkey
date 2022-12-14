import React, { useState } from 'react';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import { Button } from 'react-bootstrap';
import ErrorModal from './ErrorModal';

const authComponent = new AuthComponent({})

type Props = { url: string, agentIds: string[], agentsStartTime: Record<string, Date>, nodeLabel: string, variant?: string }

const LOG_FILE_NOT_FOUND_ERROR = "The server returned a 404 (NOT FOUND) response: " +
                                 "The requested log files do not exist."

export const AgentLogDownloadButton = ({ url, agentIds, agentsStartTime, nodeLabel, variant = 'primary' }: Props) => {
  const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(false);

  function downloadAllAgentLogs(){
    for(let agentId of agentIds){
       downloadAgentLog(agentId);
    }
  }

  function downloadAgentLog(agentId) {
    authComponent.authFetch(url + agentId)
      .then(res => {
        if (res.status === 404) {
          setNoLogFileExistsComponent(true);
        }
        return res.json()
      })
      .then(res => {
        if (res !== "") {
          download(res, logFilename(agentId), 'text/plain');
        }
      });
  }

  function logFilename(agentId) {
    let agentStartTime = agentsStartTime[agentId];
    return agentStartTime.toISOString().split(':').join('.') +
      '-' +
      nodeLabel.split(/[:/]/).join('-') +
      '.log';
  }

  function closeModal() {
    setNoLogFileExistsComponent(false);
  };

  return (<>
    <Button variant={variant} onClick={downloadAllAgentLogs}>
      Download Log
    </Button>
    <ErrorModal
      showModal={noLogFileExistsComponent}
      errorMessage={LOG_FILE_NOT_FOUND_ERROR}
      onClose={closeModal}
    />
  </>);
}

type IslandLogDownloadProps = {url: string, variant?: string}

export const IslandLogDownloadButton = ({url, variant = 'primary'}: IslandLogDownloadProps) => {
  const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(false);

  function downloadIslandLog() {
    authComponent.authFetch(url)
    .then(res => {
      if (res.status === 404) {
        setNoLogFileExistsComponent(true);
      }
      return res.json()
    })
    .then(res => {
      if (res !== "") {
        let filename = 'Island_log';
        download(res, filename, 'text/plain');
      }
    });
  }

  function closeModal() {
    setNoLogFileExistsComponent(false);
  };

  return (<>
    <Button variant={variant} onClick={downloadIslandLog}>
      Download Log
    </Button>
    <ErrorModal
      showModal={noLogFileExistsComponent}
      errorMessage={LOG_FILE_NOT_FOUND_ERROR}
      onClose={closeModal}
    />
  </>);
}
