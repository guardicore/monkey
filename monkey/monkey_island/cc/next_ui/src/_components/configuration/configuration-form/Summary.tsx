import {
    ObjectFieldTemplateProps,
    ObjectFieldTemplatePropertyType
} from '@rjsf/utils';
import React from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import { getSchemaPath } from '@/utils/common/rjsf.utils';

function handleClick(rootSchema, schema, section, onNavChanged) {
    const path = getSchemaPath(rootSchema, schema);
    path.push(section);
    console.log('handleClick', path.join('.'));
    onNavChanged(path.join('.'));
}

function generateCard(
    section: ObjectFieldTemplatePropertyType,
    schema,
    rootSchema,
    onNavChanged
) {
    return (
        <Card variant="outlined">
            <CardActionArea
                onClick={() =>
                    handleClick(rootSchema, schema, section.name, onNavChanged)
                }>
                <CardContent>
                    <Box key={section.name}>{section.name}</Box>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}

// Renders a summary view of the object
export default function SummaryObjectFieldTemplate(
    props: ObjectFieldTemplateProps
) {
    return (
        <Box>
            <h1 className="summary-title">{props.title}</h1>
            <Stack maxHeight={'100vh'} direction={'column'}>
                {props.properties.map((section) => {
                    return generateCard(
                        section,
                        props.schema,
                        props.formContext.rootSchema,
                        props.formContext.onNavChanged
                    );
                })}
            </Stack>
        </Box>
    );
}
