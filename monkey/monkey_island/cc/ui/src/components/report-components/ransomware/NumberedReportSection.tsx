import React, { ReactFragment, ReactElement } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';

type Props = {
    index: number;
    title: string;
    description: ReactFragment;
    body: ReactFragment;
};

function NumberedReportSection(props: Props): ReactElement {
    return (
        <div className="numbered-report-section">
            <Header index={props.index} title={props.title} />
            <div className="indented">
                <Description description={props.description} />
                {props.body}
            </div>
        </div>
    );
}

function Header({ index, title }: { index: number; title: string }): ReactElement {
    return (
        <h2>
            {index}. {title}
        </h2>
    );
}

function Description({ description }: { description: ReactFragment }): ReactElement {
    return (
        <div className="alert alert-secondary description">
            <FontAwesomeIcon icon={faInfoCircle} className="alert-icon" />
            <span>{description}</span>
        </div>
    );
}

export default NumberedReportSection;
