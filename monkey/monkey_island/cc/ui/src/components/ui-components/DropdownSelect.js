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
    return data.map((x, i) => generateDropdownItem(i, x));
  }

  function generateDropdownItemsFromObject(data) {
    return Object.entries(data).map(([key, value]) => generateDropdownItem(key, value));
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
