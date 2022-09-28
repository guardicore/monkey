import * as React from 'react';
import WarningIcon from '../ui-components/WarningIcon';

class WarningBox extends React.Component {

  render() {
    return (
      <div className='alert alert-info'>
        <WarningIcon style={{ 'marginRight': '5px' }} />
        {this.props.schema.info}
      </div>
    );
  }
}

export default WarningBox;
