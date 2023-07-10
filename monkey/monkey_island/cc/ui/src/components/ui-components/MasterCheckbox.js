import React from 'react';
import { Button } from 'react-bootstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckSquare } from '@fortawesome/free-solid-svg-icons';
import { faMinusSquare } from '@fortawesome/free-solid-svg-icons';
import { faSquare } from '@fortawesome/free-regular-svg-icons';

const MasterCheckboxState = {
    NONE: 0,
    MIXED: 1,
    ALL: 2
};

function MasterCheckbox(props) {
    const { title, onClick, checkboxState } = props;

    let newCheckboxIcon = faCheckSquare;

    if (checkboxState === MasterCheckboxState.NONE) {
        newCheckboxIcon = faSquare;
    } else if (checkboxState === MasterCheckboxState.MIXED) {
        newCheckboxIcon = faMinusSquare;
    }

    return (
        <div className={'master-checkbox'}>
            <Button key={`${title}-button`} variant={'link'} onClick={onClick}>
                <FontAwesomeIcon icon={newCheckboxIcon} />
            </Button>
            <span className={'header-title'}>{title}</span>
        </div>
    );
}

export { MasterCheckboxState, MasterCheckbox };
