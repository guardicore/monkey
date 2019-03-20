import '../../styles/CheckBox.scss'
import React from 'react';
import Tooltip from 'react-tooltip-lite';

class Checkbox extends React.PureComponent {

	constructor() {
		super(props);

		this.state = {
			checked: false,
			isAnimating: false,
		};

		this.toggleChecked = this.toggleChecked.bind(this);
		this.ping = this.ping.bind(this);
		this.composeStateClasses = this.composeStateClasses.bind(this);
	}

	//
	toggleChecked() {
		if (this.state.isAnimating) return false;
		this.setState({
			checked: !this.state.checked,
			isAnimating: true,
		});
	}

	//
	ping() {
		this.setState({ isAnimating: false })
	}

	//
	composeStateClasses(core) {
		let result = core;

		if (this.state.checked) { result += ' is-checked'; }
		else { result += ' is-unchecked' }

		if (this.state.isAnimating) { result += ' do-ping'; }
		return result;
	}

	//
	render() {

		const cl = this.composeStateClasses('ui-checkbox-btn');
		let tooltip = "";
    if (this.props.hasOwnProperty("tooltipContent") && this.props.hasOwnProperty("tooltipDirection")){
      tooltip = (<Tooltip content={this.props.tooltipContent} direction={this.props.tooltipDirection}
                         className="tooltip" tipContentClassName="">)
    }
  }
		return (
			<div
				className={ cl }
				onClick={ this.toggleChecked }>
          <Tooltip content={this.props.} direction="down" className="target" tipContentClassName="">
					<input className="ui ui-checkbox" type="checkbox" checked={this.state.checked} />
					{
						this.state.checked &&
							<i className="icon">
								<svg>
									<path d="M21 5q0.43 0 0.715 0.285t0.285 0.715q0 0.422-0.289 0.711l-12 12q-0.289 0.289-0.711 0.289t-0.711-0.289l-6-6q-0.289-0.289-0.289-0.711 0-0.43 0.285-0.715t0.715-0.285q0.422 0 0.711 0.289l5.289 5.297 11.289-11.297q0.289-0.289 0.711-0.289z"></path>
								</svg>
							</i>
					}
					{
						!this.state.checked &&
							<i className="icon">
								<svg>
									<path d="M19 4q0.43 0 0.715 0.285t0.285 0.715q0 0.422-0.289 0.711l-6.297 6.289 6.297 6.289q0.289 0.289 0.289 0.711 0 0.43-0.285 0.715t-0.715 0.285q-0.422 0-0.711-0.289l-6.289-6.297-6.289 6.297q-0.289 0.289-0.711 0.289-0.43 0-0.715-0.285t-0.285-0.715q0-0.422 0.289-0.711l6.297-6.289-6.297-6.289q-0.289-0.289-0.289-0.711 0-0.43 0.285-0.715t0.715-0.285q0.422 0 0.711 0.289l6.289 6.297 6.289-6.297q0.289-0.289 0.711-0.289z"></path>
								</svg>
							</i>
					}
					<label className="text">{ this.props.children }</label>
				<div className="ui-btn-ping" onTransitionEnd={this.ping}></div>
			</div>
		)
	}
}
export default Checkbox;
