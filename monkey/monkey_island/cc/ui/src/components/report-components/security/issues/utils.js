import React from 'react';

export function generateInfoBadges(data_array) {
    return data_array.map(badge_data => <span key={badge_data} className="badge badge-info"
                                              style={{margin: '2px'}}>{badge_data}</span>);
  }
