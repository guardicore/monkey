import React, {Component} from 'react';
import {Badge, Button} from 'react-bootstrap';
import * as PropTypes from 'prop-types';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faList} from '@fortawesome/free-solid-svg-icons/faList';
import ScoutSuiteRuleModal from './ScoutSuiteRuleModal';

export default class ScoutSuiteRuleButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isModalOpen: false
    }
  }

  toggleModal = () => {
    this.setState({isModalOpen: !this.state.isModalOpen});
  };

  render() {
    return (
      <>
        <ScoutSuiteRuleModal scoutsuite_rules={this.props.scoutsuite_rules}
                             scoutsuite_data={this.props.scoutsuite_data}
                             isModalOpen={this.state.isModalOpen}
                             hideCallback={this.toggleModal} />
        <div className="text-center" style={{'display': 'grid'}}>
          <Button variant={'monkey-info'} size={'lg'} onClick={this.toggleModal}>
            <FontAwesomeIcon icon={faList}/> ScoutSuite rules {this.createRuleCountBadge()}
          </Button>
        </div>
      </>);
  }

  createRuleCountBadge() {
    const ruleCount = this.props.scoutsuite_rules.length > 9 ? '9+' : this.props.scoutsuite_rules.length;
    return <Badge variant={'monkey-info-light'}>{ruleCount}</Badge>;
  }
}

ScoutSuiteRuleButton.propTypes = {
  scoutsuite_rules: PropTypes.array,
  scoutsuite_data: PropTypes.object
};
