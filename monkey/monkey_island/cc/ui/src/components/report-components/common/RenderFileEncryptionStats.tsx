import React from 'react';


function renderFileEncryptionStats(successful: number, total: number) {
  let textClassName = ""
  if(successful > 0) {
    textClassName = "text-success"
  } else {
    textClassName = "text-danger"
  }
  
  return (<p className={textClassName}>{successful} out of {total}</p>);
}

export default renderFileEncryptionStats;
