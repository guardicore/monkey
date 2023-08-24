import React, {useState} from 'react';
import Tabs from '@mui/material/Tabs';
import {Tab, Box} from '@mui/material';
import {PluginsContext} from '../ui-components/plugins-marketplace/PluginsContext';
import AvailablePlugins from '../ui-components/plugins-marketplace/AvailablePlugins';

const TabPanel = (props) => {
  const {children, value, index, ...other} = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{px: 1, py: 3}}>
          {children}
        </Box>
      )}
    </div>
  );
}
const a11yProps = (index) => {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`
  };
}

const MarketplacePage = () => {
  const [availablePlugins, setAvailablePlugins] = useState([]);
  const [installedPlugins, setInstalledPlugins] = useState([]);
  const [tabValue, setTabValue] = useState(0);

  const handleChange = (_event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <PluginsContext.Provider value={{availablePlugins, installedPlugins, setAvailablePlugins, setInstalledPlugins}}>
      <Box className="main col-xl-8 col-lg-8 col-md-9 col-sm-9 offset-xl-2 offset-lg-3 offset-md-3 offset-sm-3">
        <h1 className='page-title'>Plugins</h1>
        <Box sx={{borderBottom: 1, borderColor: 'divider'}}>
          <Tabs value={tabValue}
                onChange={handleChange}
                indicatorColor="secondary"
                textColor="inherit"
                variant="fullWidth"
                aria-label="full width tabs">
            <Tab label="Available Plugins" {...a11yProps(0)}/>
            <Tab label="Installed Plugins" {...a11yProps(1)}/>
          </Tabs>
        </Box>
        <TabPanel value={tabValue} index={0}><AvailablePlugins /></TabPanel>
        <TabPanel value={tabValue} index={1}>Installed Plugins</TabPanel>
      </Box>
    </PluginsContext.Provider>
  )
};

export default MarketplacePage;
