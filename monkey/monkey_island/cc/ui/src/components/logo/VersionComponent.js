import React from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload';
import AuthComponent from '../AuthComponent';

class VersionComponent extends AuthComponent {
    constructor(props) {
        super(props);
        this.state = {
            versionNumber: undefined,
            latestVersion: undefined,
            downloadLink: undefined
        };
    }

    componentDidMount() {
        this.authFetch('/api/island/version', {}, false)
            .then((res) => res.json())
            .then((res) => {
                this.setState({
                    versionNumber: res['version_number'],
                    latestVersion: res['latest_version'],
                    downloadLink: res['download_link']
                });
            });
    }

    newerVersionAvailable() {
        const semverGt = require('semver/functions/gt');
        if (this.state.latestVersion !== undefined && this.state.versionNumber !== undefined) {
            return semverGt(this.state.latestVersion, this.state.versionNumber);
        }
        return false;
    }

    render() {
        return (
            <div className="version-text text-center">
                Infection Monkey Version: {this.state.versionNumber}
                {this.newerVersionAvailable() ? (
                    <div>
                        <b>Newer version available!</b>
                        <br />
                        <b>
                            <a
                                rel="noopener noreferrer"
                                target="_blank"
                                href={this.state.downloadLink}>
                                Download here <FontAwesomeIcon icon={faDownload} />
                            </a>
                        </b>
                    </div>
                ) : undefined}
            </div>
        );
    }
}

export default VersionComponent;
