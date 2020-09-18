import React, {useState} from 'react';
import {Dropdown} from 'react-bootstrap';
import PropTypes from 'prop-types';

export default function DropdownSelect(props) {
  const [selectedOption, setSelectedOption] = useState(props.defaultKey);

  function generateDropdownItems(data) {
    if (Array.isArray(data)) {
      return generateDropdownItemsFromArray(data);
    } else if (typeof data === 'object') {
      return generateDropdownItemsFromObject(data);
    } else {
      throw 'Component can only generate dropdown items from arrays and objects.'
    }
  }

  function generateDropdownItemsFromArray(data) {
    const dropdownItems = [];
    for (let i = 0; i < data.length; i++) {
      dropdownItems.push(generateDropdownItem(i, data[i]));
    }
    return dropdownItems;
  }

  function generateDropdownItemsFromObject(data) {
    const dropdownItems = [];
    for (let [key, value] of Object.entries(data)) {
      dropdownItems.push(generateDropdownItem(key, value));
    }
    return dropdownItems;
  }

  function generateDropdownItem(key, value) {
    return (
      <Dropdown.Item onClick={() => { setSelectedOption(key);
                                      props.onClick(key)}}
                     active={(key === selectedOption)}
                     key={value}>
        {value}
      </Dropdown.Item>);
  }

  return (
    <>
      <Dropdown>
        <Dropdown.Toggle variant={props.variant !== undefined ? props.variant : 'success'} id='dropdown-basic'>
          {props.options[selectedOption]}
        </Dropdown.Toggle>

        <Dropdown.Menu>
          {generateDropdownItems(props.options)}
        </Dropdown.Menu>
      </Dropdown>
    </>
  )
}

DropdownSelect.propTypes = {
  options: PropTypes.oneOfType([PropTypes.object, PropTypes.array]),
  defaultKey: PropTypes.oneOfType([PropTypes.string,PropTypes.number]),
  onClick: PropTypes.func
}
