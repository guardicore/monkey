import React from 'react';
import AuthComponent from "../AuthComponent";
import {Icon} from 'react-fa';

class VersionComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      currentVersion: undefined,
      newerVersion: undefined,
      downloadLink: undefined
    }
  }

  componentDidMount() {
    this.authFetch('/api/version-update')
      .then(res => res.json())
      .then(res => {
        this.setState({
          currentVersion: res['current_version'],
          newerVersion: res['newer_version'],
          downloadLink: res['download_link'],
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
              <b><a target="_blank" href={this.state.downloadLink}>Download here <Icon name="download"/></a></b>
            </div>
            :
            undefined
        }
      </div>
    );
  }
}


export default VersionComponent;
