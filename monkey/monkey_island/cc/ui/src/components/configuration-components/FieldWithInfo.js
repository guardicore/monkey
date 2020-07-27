import ObjectField from 'react-jsonschema-form-bs4/lib/components/fields/ArrayField';
import * as React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faInfoCircle} from '@fortawesome/free-solid-svg-icons/faInfoCircle';

class FieldWithInfo extends React.Component {

  render() {
    return (
      <>
        <div className='alert alert-info'>
          <FontAwesomeIcon icon={faInfoCircle} style={{'marginRight': '5px'}}/>
          {this.props.schema.info}
        </div>
        <ObjectField {...this.props} />
      </>);
  }
}

export default FieldWithInfo;
