import '../../styles/components/Checkbox.scss'
import React from 'react';

class CheckboxComponent extends React.PureComponent {

  componentDidUpdate(prevProps) {
    if (this.props.checked !== prevProps.checked) {
      this.setState({checked: this.props.checked});
    }
  }

  /*
  Parent component can pass a name and a changeHandler (function) for this component in props.
	changeHandler(name, checked) function will be called with these parameters:
	this.props.name (the name of this component) and
	this.state.checked (boolean indicating if this component is checked or not)

	this.props.status (int) adds a class "status-x" to this checkbox. Used for styling.
  */
  constructor(props) {
    super(props);
    if (Object.prototype.hasOwnProperty.call(this.props, 'status')){
      this.status = this.props.status;
    } else {
      this.status = false
    }
    this.state = {
      status: this.status,
      checked: this.props.checked,
      necessary: this.props.necessary,
      isAnimating: false
    };
    this.toggleChecked = this.toggleChecked.bind(this);
    this.stopAnimation = this.stopAnimation.bind(this);
    this.composeStateClasses = this.composeStateClasses.bind(this);
  }

  //Toggles component.
  toggleChecked() {
    if (this.state.isAnimating) {
      return false;
    }
    this.setState({
      checked: !this.state.checked,
      isAnimating: true
    }, () => {
      this.props.changeHandler ? this.props.changeHandler(this.props.name, this.state.checked) : null
    });
  }

  // Stops ping animation on checkbox after click
  stopAnimation() {
    this.setState({isAnimating: false})
  }

  // Creates class string for component
  composeStateClasses(core) {
    let result = core;
    if (this.state.status !== false) {
      result += ' status-'+this.state.status;
    }
    if (this.state.necessary) {
      return result + ' blocked'
    }
    if (this.state.checked) {
      result += ' is-checked';
    } else {
      result += ' is-unchecked'
    }
    if (this.state.isAnimating) {
      result += ' do-ping';
    }
    return result;
  }

  render() {
    const cl = this.composeStateClasses('ui-checkbox-btn');
    return (
      <div
        className={cl}
        onClick={this.state.necessary ? void (0) : this.toggleChecked}>
        <input className='ui ui-checkbox'
               type='checkbox' value={this.state.checked}
               name={this.props.name}/>
        <label className='text'>{this.props.children}</label>
        <div className='ui-btn-ping' onTransitionEnd={this.stopAnimation}/>
      </div>
    )
  }
}

export default CheckboxComponent;
