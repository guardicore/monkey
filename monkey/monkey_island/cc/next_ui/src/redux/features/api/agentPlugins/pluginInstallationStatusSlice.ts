import { createSlice } from '@reduxjs/toolkit';
import { RootState } from '@/redux/store';

export enum InstallationStatus {
    PENDING = 'PENDING',
    SUCCESS = 'SUCCESS',
    FAILURE = 'FAILURE'
}

type InstallationStatusActionPayload = {
    pluginId: string;
    status: InstallationStatus;
};

const pluginInstallationStatusSlice = createSlice({
    name: 'agentPlugins/installationStatus',
    initialState: {},
    reducers: {
        setPluginInstallationStatus: (
            state,
            action: { payload: InstallationStatusActionPayload }
        ) => {
            state[action.payload.pluginId] = action.payload.status;
        }
    }
});

export const selectStatusByPluginId = (
    state: RootState,
    pluginId: string
): InstallationStatus => state[pluginInstallationStatusSlice.name][pluginId];

export const { setPluginInstallationStatus } =
    pluginInstallationStatusSlice.actions;

export default pluginInstallationStatusSlice;
