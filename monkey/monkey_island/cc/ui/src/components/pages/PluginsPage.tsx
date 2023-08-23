import React, {useState} from 'react';
import { Col, Nav } from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import {useNavigate} from 'react-router-dom';
import AvailablePlugins from '../plugin-components/AvailablePlugins';
import InstalledPlugins from '../plugin-components/InstalledPlugins';
import UploadPlugin from '../plugin-components/UploadPlugin';


// TODO: Make a component for a tab pane
// - See if a tab pane component already exists (one does - @mui/material/Tabs, but it's visually inconsistent with our other tabs)
function PluginsPage (props) {
    const sections = ['available', 'installed', 'upload'];
    const [selectedSection, setSelectedSection] = useState(selectTab(sections));
    const orderedSections = [{key: 'available', title: 'Available Plugins'}, {key: 'installed', title: 'Installed Plugins'}, {key: 'upload', title: 'Upload New Plugin'}];
    const authComponent = new AuthComponent({});

    function selectTab(tabs) {
        let url = window.location.href;
        for (let tab_name in tabs) {
          if (Object.prototype.hasOwnProperty.call(sections, tab_name) && url.endsWith(sections[tab_name])) {
            return sections[tab_name];
          }
        }
        return 'installed'; // The default tab
    };

    function renderNav() {
        let navigate = useNavigate();
        return (
            <Nav variant='tabs'
                 fill
                 activeKey={selectedSection}
                 onSelect={(key) => {
                   setSelectedSection(key);
                   navigate("/plugins/" + key);
                 }}
                 className={'report-nav'}>
              {orderedSections.map(section => renderNavButton(section))}
            </Nav>)
    };

    function renderNavButton(section) {
        return (
          <Nav.Item key={section.key}>
            <Nav.Link key={section.key}
                      eventKey={section.key}
                      onSelect={() => {
                      }}>
              {section.title}
            </Nav.Link>
          </Nav.Item>)
      };

    function renderContent() {
        switch (selectedSection) {
            case 'available':
                return <AvailablePlugins />;
            case 'installed':
                return <InstalledPlugins />;
            case 'upload':
                return <UploadPlugin />;
        }
    };

    return (
        <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
              lg={{offset: 3, span: 9}} xl={{offset: 2, span: 10}}
              className={'main'}>
          <h1 className='page-title'>Plugins</h1>
          {renderNav()}
          <div style={{'fontSize': '1.2em'}}>
            {renderContent()}
          </div>
        </Col>
    );
}

export default PluginsPage;
