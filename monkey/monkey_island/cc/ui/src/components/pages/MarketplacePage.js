import React, {useContext, useState} from 'react';
import Tabs from '@mui/material/Tabs';
import {Tab, Box, Badge, Stack} from '@mui/material';
import {PluginsContext} from '../contexts/plugins/PluginsContext';
import AvailablePlugins from '../ui-components/plugins-marketplace/AvailablePlugins';
import InstalledPlugins from '../ui-components/plugins-marketplace/InstalledPlugins';
import classes from '../../styles/pages/Marketplace.module.scss';
import UploadNewPlugin from '../ui-components/plugins-marketplace/UploadNewPlugin';

const TabPanel = (props) => {
  const {children, value, index, ...other} = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      style={{minHeight: 0}}
      {...other}
    >
      {value === index && (
        <Box sx={{px: 1, py: 3, height: '100%'}}>
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
  const {numberOfPluginsThatRequiresUpdate, refreshInstalledPlugins} = useContext(PluginsContext);
  const [successfullyInstalledPluginsIds, setSuccessfullyInstalledPluginsIds] = useState([]);
  const [pluginsInInstallationProcess, setPluginsInInstallationProcess] = useState([]);
  const [successfullyUpdatedPluginsIds, setSuccessfullyUpdatedPluginsIds] = useState([]);
  const [pluginsInUpdateProcess, setPluginsInUpdateProcess] = useState([]);
  const [successfullyUninstalledPluginsIds, setSuccessfullyUninstalledPluginsIds] = useState([]);
  const [pluginsInUninstallProcess, setPluginsInUninstallProcess] = useState([]);

  const [tabValue, setTabValue] = useState(0);

  const handleChange = (_event, newValue) => {
    setTabValue(newValue);
    if(pluginsInInstallationProcess.length === 0){
      setSuccessfullyInstalledPluginsIds([]);
    }
    setSuccessfullyUpdatedPluginsIds([]);
    setSuccessfullyUninstalledPluginsIds([]);
    refreshInstalledPlugins();
  }

  const installedPluginsLabel = <div>
    <Badge badgeContent={numberOfPluginsThatRequiresUpdate} color="error">
      <span id="installed-plugins-tab-label">Installed Plugins</span>
    </Badge>
  </div>

  return (
      <Box id={classes['marketplace-page']} className="main col-xl-8 col-lg-8 col-md-9 col-sm-9 offset-xl-2 offset-lg-3 offset-md-3 offset-sm-3" maxHeight={'100vh'}>
        <Stack height='100%'>
        <h1 className='page-title'>Plugins</h1>
        <Box sx={{borderBottom: 1, borderColor: 'divider'}}>
          <Tabs value={tabValue}
                onChange={handleChange}
                indicatorColor="secondary"
                textColor="inherit"
                variant="fullWidth"
                aria-label="full width tabs">
            <Tab label="Available Plugins" {...a11yProps(0)}/>
            <Tab label={installedPluginsLabel} {...a11yProps(1)}/>
            <Tab label="Upload New Plugin" {...a11yProps(2)}/>
          </Tabs>
        </Box>
        <TabPanel value={tabValue} index={0}>
          <AvailablePlugins
            successfullyInstalledPluginsIds={successfullyInstalledPluginsIds}
            setSuccessfullyInstalledPluginsIds={setSuccessfullyInstalledPluginsIds}
            pluginsInInstallationProcess={pluginsInInstallationProcess}
            setPluginsInInstallationProcess={setPluginsInInstallationProcess} />
        </TabPanel>
        <TabPanel value={tabValue} index={1}>
          <InstalledPlugins
              successfullyUpdatedPluginsIds={successfullyUpdatedPluginsIds}
              setSuccessfullyUpdatedPluginsIds={setSuccessfullyUpdatedPluginsIds}
              pluginsInUpdateProcess={pluginsInUpdateProcess}
              setPluginsInUpdateProcess={setPluginsInUpdateProcess}
              successfullyUninstalledPluginsIds={successfullyUninstalledPluginsIds}
              setSuccessfullyUninstalledPluginsIds={setSuccessfullyUninstalledPluginsIds}
              pluginsInUninstallProcess={pluginsInUninstallProcess}
              setPluginsInUninstallProcess={setPluginsInUninstallProcess} />
        </TabPanel>
        <TabPanel value={tabValue} index={2}><UploadNewPlugin/></TabPanel>
        </Stack>
      </Box>
  )
};

export default MarketplacePage;
