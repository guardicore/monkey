import AppSidebar from '@/_components/app-nav/app-sidebar/AppSidebar';
import SidebarItem from '@/_components/app-nav/app-sidebar/SidebarItem';
import ExtensionIcon from '@mui/icons-material/Extension';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { useRouter, useSelectedLayoutSegment } from 'next/navigation';
import PluginPages from '@/app/(protected)/plugins/pluginPages';

export default function PluginSidebar() {
    const urlSegment = useSelectedLayoutSegment();
    const router = useRouter();

    const sidebarItems = [
        <SidebarItem
            key={PluginPages.AvailablePlugins}
            icon={<ExtensionIcon />}
            name={'Available Plugins'}
            onClick={() =>
                router.push(`/plugins/${PluginPages.AvailablePlugins}`)
            }
            selected={urlSegment === PluginPages.AvailablePlugins}
        />,
        <SidebarItem
            key={PluginPages.InstalledPlugins}
            icon={<DownloadDoneIcon />}
            name={'Installed Plugins'}
            onClick={() =>
                router.push(`/plugins/${PluginPages.InstalledPlugins}`)
            }
            selected={urlSegment === PluginPages.InstalledPlugins}
        />,
        <SidebarItem
            key={PluginPages.Upload}
            icon={<FileUploadIcon />}
            name={'Upload'}
            onClick={() => router.push(`/plugins/${PluginPages.Upload}`)}
            selected={urlSegment === PluginPages.Upload}
            prependDivider={true}
        />
    ];
    return <AppSidebar items={sidebarItems} />;
}
