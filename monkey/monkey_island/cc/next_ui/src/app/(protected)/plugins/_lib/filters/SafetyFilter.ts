import { AgentPlugin } from '@/redux/features/api/agentPlugins/types';

export const filterOutDangerousPlugins = (plugins: AgentPlugin[]) => {
    return plugins.filter((plugin) => plugin.safe);
};
