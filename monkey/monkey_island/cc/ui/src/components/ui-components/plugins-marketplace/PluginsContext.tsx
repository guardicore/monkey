import React, {createContext} from 'react';

type PluginsContextType = {
    availablePlugins: any;
    installedPlugins: any;
    refreshAvailablePlugins: (force: boolean) => void;
    refreshInstalledPlugins: () => void;
}

export const PluginsContext = createContext<Partial<PluginsContextType>>({});
