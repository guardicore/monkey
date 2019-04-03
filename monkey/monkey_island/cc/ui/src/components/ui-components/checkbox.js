import '../../styles/Checkbox.scss'
import React from 'react';

class Checkbox extends React.PureComponent {

  componentDidUpdate(prevProps) {
    if (this.props.checked !== prevProps.checked) {
      this.setState({checked: this.props.checked});
    }
  }

	constructor(props) {
		super(props);
		this.state = {
			checked: this.props.checked,
      necessary: this.props.necessary,
			isAnimating: false
		};
		this.toggleChecked = this.toggleChecked.bind(this);
		this.ping = this.ping.bind(this);
		this.composeStateClasses = this.composeStateClasses.bind(this);
	}
	
	toggleChecked() {
		if (this.state.isAnimating) return false;
		this.setState({
			checked: !this.state.checked,
			isAnimating: true,
		}, () => { this.props.changeHandler(this.props.name, this.state.checked)});
	}

	// Stops animation
	ping() {
		this.setState({ isAnimating: false })
	}

	// Creates class string for component
	composeStateClasses(core) {
		let result = core;
    if (this.state.necessary){
      return result + ' blocked'
    }
		if (this.state.checked) { result += ' is-checked'; }
		else { result += ' is-unchecked' }

		if (this.state.isAnimating) { result += ' do-ping'; }
		return result;
	}

	render() {
		const cl = this.composeStateClasses('ui-checkbox-btn');
		return (
			<div
				className={ cl }
				onClick={ this.state.necessary ? void(0) : this.toggleChecked}>
					<input className="ui ui-checkbox"
                 type="checkbox" value={this.state.checked}
                 name={this.props.name}/>
					<label className="text">{ this.props.children }</label>
				<div className="ui-btn-ping" onTransitionEnd={this.ping}></div>
			</div>
		)
	}
}

export default Checkbox;
