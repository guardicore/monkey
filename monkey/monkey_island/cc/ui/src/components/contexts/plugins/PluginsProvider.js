import React from 'react';
import {PluginsContext} from './PluginsContext';
import { Outlet } from 'react-router-dom';

const PluginsProvider = (props) => {
  const {value} = {...props};

  return (
    <PluginsContext.Provider value={value}>
      <Outlet />
    </PluginsContext.Provider>
  )
}

export default PluginsProvider;
