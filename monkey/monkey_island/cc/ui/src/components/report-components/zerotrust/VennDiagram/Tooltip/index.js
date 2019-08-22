import React from 'react'
import PropTypes from 'prop-types';

class Tooltip extends React.Component{

    render() {
        
        const {prefix, bcolor, top, left, display, html } = this.props;

        const style = {
            
            backgroundColor: bcolor,
            border : '1px solid #FFFFFF',
            borderRadius: '2px',
            fontSize: 10,
            padding: 8,
            display,
            opacity: 0.9,
            position: 'fixed',
            top,
            left,
            pointerEvents: 'none'
            
        };

        return (
            
            <div className='tooltip' style={style}>
             {html.split('\n').map((i_, key_) => { return <div key={prefix + 'Element' + key_}>{i_}</div>; })}
            </div>
                                                  
        );
        
    }
    
}

Tooltip.propTypes = {
        
    prefix: PropTypes.string,
    bcolor: PropTypes.string,
    top: PropTypes.number,
    left: PropTypes.number,
    display: PropTypes.string,
    html: PropTypes.string
        
}
                                   
export default Tooltip;