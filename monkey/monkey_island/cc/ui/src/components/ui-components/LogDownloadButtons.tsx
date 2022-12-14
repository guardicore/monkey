import React, { useState } from 'react';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import { Button } from 'react-bootstrap';
import Error404Modal from './Error404Modal';

const authComponent = new AuthComponent({})

type Props = { url: string, filename: string, variant?: string }


export const AgentLogDownloadButton = ({ url, filename, variant = 'primary' }: Props) => {
  const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(false);

  function downloadAgentLog() {
    authComponent.authFetch(url)
      .then(res => {
        if (res.status === 404) {
          setNoLogFileExistsComponent(true);
        }
        return res.json()
      })
      .then(res => {
        if (res !== "") {
          download(res, filename, 'text/plain');
        }
      });
  }

  function closeModal() {
    setNoLogFileExistsComponent(false);
  };

  return (<>
    <Button variant={variant} onClick={downloadAgentLog}>
      Download Log
    </Button>
    <Error404Modal
      showModal={noLogFileExistsComponent}
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
    <Error404Modal
      showModal={noLogFileExistsComponent}
      onClose={closeModal}
    />
  </>);
}
