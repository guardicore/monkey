import { ObjectFieldTemplateProps } from '@rjsf/utils';
import { Form } from '@rjsf/mui';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import { getSubSchema } from '@/utils/common/rjsf.utils';
import SummaryObjectFieldTemplate from './Summary';
import _ from 'lodash';

function* generateBreadcrumbLinks(rootSchema, path, onNavChanged) {
    const parts = path.split('.');
    let schema = rootSchema;
    const linkPath: any[] = [];

    for (const part of parts) {
        schema = schema.properties[part];
        linkPath.push(part);
        const crumbPath = linkPath.join('.');
        yield (
            <Link
                underline="hover"
                key={part}
                color="inherit"
                href="#"
                onClick={() => onNavChanged(crumbPath)}>
                {schema.title}
            </Link>
        );
    }
}

function buildBreadcrumbs(rootSchema, path, onNavChanged) {
    const links = Array.from(
        generateBreadcrumbLinks(rootSchema, path, onNavChanged)
    );
    return (
        <Breadcrumbs
            aria-label="breadcrumb"
            sx={{ marginTop: '5em', marginBottom: '1em' }}>
            {links.map((link) => {
                return link;
            })}
        </Breadcrumbs>
    );
}

// Renders a focused view of the object
// TODO: Figure out how, or if/when content should be limited. Only on objects?
// - Could potentially override templates: https://github.com/rjsf-team/react-jsonschema-form/issues/3333
export default function FocusedObjectFieldTemplate(
    props: ObjectFieldTemplateProps
) {
    // Although the Focused view props remain unchanged, the formData is updated
    // based on the selectedPath
    return (
        <Box>
            {buildBreadcrumbs(
                props.formContext.rootSchema,
                props.formContext.selectedPath,
                props.formContext.onNavChanged
            )}
            <h1 className="summary-title">{'Focused:' + props.title}</h1>
            <Form
                schema={getSubSchema(
                    props.formContext.rootSchema,
                    props.formContext.selectedPath
                )}
                formData={_.get(props.formData, props.formContext.selectedPath)}
                formContext={{ ...props.formContext }}
                ObjectFieldTemplate={SummaryObjectFieldTemplate}
                uiSchema={{
                    'ui:ObjectFieldTemplate': SummaryObjectFieldTemplate
                }}
                validator={props.registry.schemaUtils.getValidator()}
                liveValidate={true}></Form>
        </Box>
    );
}
