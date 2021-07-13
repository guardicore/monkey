import React from 'react';


function renderFileEncryptionStats(successful: number, total: number) {
  if(successful > 0){
    return (<p className={"text-success"}>{successful} out of {total}</p>);
  } else {
    return (<p className={"text-danger"}>{successful} out of {total}</p>);
  }
}

export default renderFileEncryptionStats;
