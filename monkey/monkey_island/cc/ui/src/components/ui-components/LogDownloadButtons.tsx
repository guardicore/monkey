import React from 'react';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import { Button } from 'react-bootstrap';

const authComponent = new AuthComponent({})

type Props = { url: string, filename: string, variant?: string }



export const AgentLogDownloadButton = ({ url, filename, variant = 'primary' }: Props) => {
  function downloadAgentLog() {
    authComponent.authFetch(url)
      .then(res => res.json())
      .then(res => {
        let logContent = res;
        download(logContent, filename, 'text/plain');
      });
  }

  return (<Button variant={variant}
    onClick={downloadAgentLog}>
    Download Log
  </Button>);
}


export const IslandLogDownloadButton = ({ url, variant = 'primary' }: Props) => {
  function downloadIslandLog() {
    authComponent.authFetch(url)
      .then(res => res.json())
      .then(res => {
        let filename = 'Island_log';
        let logContent = res;
        download(logContent, filename, 'text/plain');
      });
  }
  return (<Button variant={variant}
    onClick={downloadIslandLog}>
    Download Log
  </Button>);
}
