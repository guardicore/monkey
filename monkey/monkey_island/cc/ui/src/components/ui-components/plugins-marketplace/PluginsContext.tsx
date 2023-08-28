import React, {createContext} from 'react';

type PluginsContextType = {
    availablePlugins: any;
    installedPlugins: any;
    refreshAvailablePlugins: () => void;
    refreshInstalledPlugins: () => void;
}

export const PluginsContext = createContext<Partial<PluginsContextType>>({});
