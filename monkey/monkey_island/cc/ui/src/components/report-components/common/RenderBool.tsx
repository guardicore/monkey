import React from 'react';


function renderBool(val: Boolean) {

    if(val === true){
      return (<p className={"text-success"}>Yes</p>);
    } else {
      return (<p className={"text-danger"}>No</p>);
    }
}

export default renderBool;
