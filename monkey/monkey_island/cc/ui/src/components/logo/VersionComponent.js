import React from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons/faDownload';

class VersionComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentVersion: undefined,
      newerVersion: undefined,
      downloadLink: undefined
    }
  }

  componentDidMount() {
    fetch('/api/version-update') // This is not authenticated on purpose
      .then(res => res.json())
      .then(res => {
        this.setState({
          currentVersion: res['current_version'],
          newerVersion: res['newer_version'],
          downloadLink: res['download_link']
        });
      });
  }

  render() {
    return (
      <div className="version-text text-center">
        Infection Monkey Version: {this.state.currentVersion}
        {
          this.state.newerVersion ?
            <div>
              <b>Newer version available!</b>
              <br/>
              <b><a rel="noopener noreferrer" target="_blank" href={this.state.downloadLink}>Download here <FontAwesomeIcon icon={faDownload}/></a></b>
            </div>
            :
            undefined
        }
      </div>
    );
  }
}


export default VersionComponent;
