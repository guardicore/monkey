import React from 'react';
import {InputGroup, FormControl} from 'react-bootstrap';

class SensitiveTextInput extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      hidden: false
    };
  }

  toggleShow = () => {
    this.setState({hidden: ! this.state.hidden});
  }

  onChange(e) {
    var value = e.target.value;
    return this.props.onChange(value === '' ? this.props.options.emptyValue : value);
  }

  render() {
    return (
    <div>
      <InputGroup>
        <FormControl
            value={this.props.value || ''}
            type={this.state.hidden ? 'text' : 'password'}
            onChange={(event) => this.onChange(event)}
        />
        <InputGroup.Append>
          <InputGroup.Text onClick={this.toggleShow} >
            <i className={this.state.hidden ? 'fas fa-eye-slash' : 'fas fa-eye'}></i>
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
    </div>
    );
  }
}

export default SensitiveTextInput;
