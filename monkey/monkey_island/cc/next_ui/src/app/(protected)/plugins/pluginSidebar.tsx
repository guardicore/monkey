import AppSidebar from '@/_components/app-nav/app-sidebar/AppSidebar';
import SidebarItem from '@/_components/app-nav/app-sidebar/SidebarItem';
import ExtensionIcon from '@mui/icons-material/Extension';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export default function PluginSidebar() {
    const sidebarItems = [
        <SidebarItem
            key={'available'}
            icon={<ExtensionIcon />}
            name={'Available Plugins'}
        />,
        <SidebarItem
            key={'installed'}
            icon={<DownloadDoneIcon />}
            name={'Installed Plugins'}
        />,
        <SidebarItem
            key={'upload'}
            icon={<FileUploadIcon />}
            name={'Upload'}
            prependDivider={true}
        />
    ];
    return <AppSidebar items={sidebarItems} />;
}
