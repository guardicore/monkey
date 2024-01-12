import { ObjectFieldTemplateProps } from '@rjsf/utils';
import React, { useState } from 'react';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';

// Renders each property in the schema as a tab
export default function TabsTemplate(props: ObjectFieldTemplateProps) {
    // console.log('TabsTemplate', props);
    const [selectedTab, setSelectedTab] = useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setSelectedTab(newValue);
    };

    const renderSelectedSection = () => {
        console.log('Tab properties', props.properties[selectedTab]);
        return props.properties[selectedTab].content;
        // const newProps = {...props.properties[selectedTab].content.props.schema};
        // return <Summary {...newProps} />;
    };

    return (
        <Stack maxHeight={'100vh'} direction={'row'}>
            <Tabs
                value={selectedTab}
                orientation="vertical"
                onChange={handleChange}
                style={{ marginRight: '2em' }}
                className={'config-nav'}>
                {props.properties.map((section) => {
                    return <Tab key={section.name} label={section.name} />;
                })}
            </Tabs>
            <Box overflow={'auto'}>{renderSelectedSection()}</Box>
        </Stack>
    );
}
