import React from 'react';
import {InputGroup, FormControl} from 'react-bootstrap';
import '../../styles/components/HideInput.scss'

class HideInput extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      hidden: false
    };
    this.toggleShow = this.toggleShow.bind(this);
  }

  toggleShow() {
    this.setState({hidden: ! this.state.hidden});
  }

  onChange(e) {
    var value = e.target.value;
    return this.props.onChange(value === '' ? this.props.options.emptyValue : value);
  }

  render() {
    return (
    <div>
      <InputGroup className='mb-3'>
        <FormControl
            value={this.props.value || ''}
            type={this.state.hidden ? 'text' : 'password'}
            onChange={(event) => this.onChange(event)}
        />
        <InputGroup.Append>
          <InputGroup.Text>
            <i onClick={this.toggleShow} className={this.state.hidden ? 'fas fa-eye-slash' : 'fas fa-eye'}></i>
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
    </div>
    );
  }
}

export default HideInput;
