import React, { useEffect, useState } from 'react';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import { Button } from 'react-bootstrap';
import ErrorModal from './ErrorModal';

const authComponent = new AuthComponent({});

type Props = {
    url: string;
    agentIds: string[];
    agentsStartTime: Record<string, Date>;
    nodeLabel: string;
    variant?: string;
    disabled?: boolean;
};

const LOG_FILE_NOT_FOUND_ERROR =
    'The server returned a 404 (NOT FOUND) response: ' + 'The requested log files do not exist.';

export const AgentLogDownloadButton = ({
    url,
    agentIds,
    agentsStartTime,
    nodeLabel,
    variant = 'primary',
    disabled = false
}: Props) => {
    const [nonExistingAgentLogsIds, setNonExistingAgentLogsIds] = useState([]);
    const [errorDetails, setErrorDetails] = useState(null);

    useEffect(() => {
        setErrorDetails(getAgentErrorDetails());
    }, [nonExistingAgentLogsIds]);

    function downloadAllAgentLogs() {
        for (let agentId of agentIds) {
            downloadAgentLog(agentId);
        }
    }

    function downloadAgentLog(agentId) {
        authComponent
            .authFetch(url + agentId, {}, true)
            .then((res) => {
                if (res.status === 404) {
                    setNonExistingAgentLogsIds((prevIds) => [...prevIds, agentId]);
                }
                return res.json();
            })
            .then((res) => {
                if (res !== '') {
                    download(res, logFilename(agentId), 'text/plain');
                }
            });
    }

    function logFilename(agentId) {
        let agentStartTime = agentsStartTime[agentId];
        return (
            agentStartTime.toISOString().split(':').join('.') +
            '-' +
            nodeLabel.split(/[:/]/).join('-') +
            '.log'
        );
    }

    function getAgentErrorDetails() {
        let agentLogFileNotFoundErrorDetails =
            'The log files do not exists from the following agents: \n';
        for (let agentId of nonExistingAgentLogsIds) {
            agentLogFileNotFoundErrorDetails = agentLogFileNotFoundErrorDetails.concat(
                agentId + '\n'
            );
        }

        return agentLogFileNotFoundErrorDetails;
    }

    function closeModal() {
        setNonExistingAgentLogsIds([]);
    }

    return (
        <>
            <Button variant={variant} onClick={downloadAllAgentLogs} disabled={disabled}>
                Download Log
            </Button>
            <ErrorModal
                showModal={nonExistingAgentLogsIds.length !== 0}
                errorMessage={LOG_FILE_NOT_FOUND_ERROR}
                errorDetails={errorDetails}
                onClose={closeModal}
            />
        </>
    );
};

type IslandLogDownloadProps = {
    url: string;
    variant?: string;
    disabled?: boolean;
};

export const IslandLogDownloadButton = ({
    url,
    variant = 'primary',
    disabled = false
}: IslandLogDownloadProps) => {
    const [noLogFileExistsComponent, setNoLogFileExistsComponent] = useState(false);

    function downloadIslandLog() {
        authComponent
            .authFetch(url, {}, true)
            .then((res) => {
                if (res.status === 404) {
                    setNoLogFileExistsComponent(true);
                }
                return res.json();
            })
            .then((res) => {
                if (res !== '') {
                    let filename = 'Island_log';
                    download(res, filename, 'text/plain');
                }
            });
    }

    function closeModal() {
        setNoLogFileExistsComponent(false);
    }

    return (
        <>
            <Button variant={variant} onClick={downloadIslandLog} disabled={disabled}>
                Download Log
            </Button>
            <ErrorModal
                showModal={noLogFileExistsComponent}
                errorMessage={LOG_FILE_NOT_FOUND_ERROR}
                onClose={closeModal}
            />
        </>
    );
};
