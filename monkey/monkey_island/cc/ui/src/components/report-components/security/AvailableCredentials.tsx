import {getAllUsernames, getAllSecrets} from '../credentialParsing';
import React from 'react';

const AvailableCredentials = (props) => {
  let allUsernames = getAllUsernames(props.stolen, props.configured);
  let allSecrets = getAllSecrets(props.stolen, props.configured);
  return (
  allUsernames.length > 0 ?
    <>
      <p>
        Usernames available for brute-forcing:
      </p>
      <ul>
        {allUsernames.map(x => <li key={x}>{x}</li>)}
      </ul>
      <p>
        Credentials available for brute-forcing:
      </p>
      <ul>
        {allSecrets.map((x, index) => <li
          key={index}>{x['title']}: {x['content'].substr(0, 3) + '******'}</li>)}
      </ul>
    </>
    :
    <p>
      No credentials available for brute forcing.
    </p>
  )
}

export default AvailableCredentials;
