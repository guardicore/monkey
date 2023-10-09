const authFetch = (url: string, options?: any) => {
    const token = localStorage.getItem('authentication_token');
    const headers = {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
        "ngrok-skip-browser-warning": "69420"
    };
    return fetch(url, { ...options, headers: headers });
}

export default authFetch;
