import React, { useState } from 'react';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import { Button } from 'react-bootstrap';

const authComponent = new AuthComponent({})

type Props = { url: string, filename: string, variant?: string }


export const AgentLogDownloadButton = ({ url, filename, variant = 'primary' }: Props) => {
  const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(<></>);

  function downloadAgentLog() {
    authComponent.authFetch(url)
      .then(res => {
        if (res.status === 404) {
          setNoLogFileExistsComponent(
            <p style={{'marginTop': '1em', 'marginBottom': '1em', 'color': 'red'}}>
              The server could not find the requested log file.
            </p>
          );
        }
        return res.json()
      })
      .then(res => {
        if (res !== "") {
          download(res, filename, 'text/plain');
        }
      });
  }

  return (<>
    <Button variant={variant} onClick={downloadAgentLog}>
      Download Log
    </Button>
    {noLogFileExistsComponent}
  </>);
}

type IslandLogDownloadProps = {url: string, variant?: string}

export const IslandLogDownloadButton = ({url, variant = 'primary'}: IslandLogDownloadProps) => {
  const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(<></>);
  function downloadIslandLog() {
    authComponent.authFetch(url)
    .then(res => {
      if (res.status === 404) {
        setNoLogFileExistsComponent(
          <p style={{'marginTop': '1em', 'marginBottom': '1em', 'color': 'red'}}>
            The server could not find the requested log file.
          </p>
        );
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
  return (<>
    <Button variant={variant} onClick={downloadIslandLog}>
      Download Log
    </Button>
    {noLogFileExistsComponent}
  </>);
}
