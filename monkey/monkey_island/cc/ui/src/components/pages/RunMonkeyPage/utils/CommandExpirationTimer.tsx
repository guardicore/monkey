import React from 'react';

export function CommandExpirationTimer({ minutes, seconds }) {

    function formatDigits(number) {
      return number.toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false})
    }

    function generateText() {
      if (minutes === 0 && seconds === 0) {
        return 'Command expired';
      } else {
        return 'Command expires in: ' + formatDigits(minutes) + ':' + formatDigits(seconds);
      }
    }

    return (
      <div style={{textAlign: 'right'}}>
        {generateText()}
      </div>
    );
}
