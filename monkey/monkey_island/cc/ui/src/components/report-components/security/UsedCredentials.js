import {getAllUsernames, getAllSecrets} from '../credentialParsing';
import React from 'react';

class UsedCredentials extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    let allUsernames = getAllUsernames(this.props.stolen, this.props.configured);
    let allSecrets = getAllSecrets(this.props.stolen, this.props.configured);
    return (
    allUsernames.length > 0 ?
      <>
        <p>
          Usernames used for brute-forcing:
        </p>
        <ul>
          {allUsernames.map(x => <li key={x}>{x}</li>)}
        </ul>
        <p>
          Credentials used for brute-forcing:
        </p>
        <ul>
          {allSecrets.map((x, index) => <li
            key={index}>{x['title']}: {x['content'].substr(0, 3) + '******'}</li>)}
        </ul>
      </>
      :
      <p>
        No credentials were used.
      </p>
  )

  }

}

export default UsedCredentials;
