import AuthComponent from './AuthComponent';
import React from 'react';

export class Response {
  body: any
  status: number

  constructor(body: any, status: number) {
    this.body = body
    this.status = status
  }
}

export enum APIEndpoint {
  agent_otp = '/api/agent-otp',
  agents = '/api/agents',
  machines = '/api/machines',
  nodes = '/api/nodes',
  agentEvents = '/api/agent-events',
  monkey_exploitation = '/api/exploitations/monkey',
  stolenCredentials = '/api/propagation-credentials/stolen-credentials',
  linuxMasque = '/api/agent-binaries/linux/masque',
  windowsMasque = '/api/agent-binaries/windows/masque',
  installAgentPlugin = '/api/install-agent-plugin',
  uninstallAgentPlugin = '/api/uninstall-agent-plugin'
}

class IslandHttpClient extends AuthComponent {
  put(endpoint: string, contents: any, refreshToken: boolean = false): Promise<Response> {
    const headers = {'Content-Type': 'application/octet-stream'};
    return this._put(endpoint, contents, headers, refreshToken);
  }

  putJSON(endpoint: string, contents: any, refreshToken: boolean = false): Promise<Response> {
    const headers = {'Content-Type': 'application/json'};
    return this._put(endpoint, JSON.stringify(contents), headers, refreshToken);
  }

  _put(endpoint: string, contents: any, headers: Record<string, any>={}, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    return this.authFetch(endpoint,
      {
        method: 'PUT',
        headers: headers,
        body: contents
      },
      refreshToken
    )
      .then(res => {
        status = res.status;
        return res
      })
      .then(res => new Response(res, status));
  }

  getJSON(endpoint: APIEndpoint, args: Record<string, any>={}, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    return this.get(endpoint, args, refreshToken)
      .then(res => {
        status = res.status;
        return res.body.json()
      })
      .then(res => new Response(res, status));
  }

  get(endpoint: APIEndpoint, args: Record<string, any>={}, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    let params = new URLSearchParams(args);
    let url = String(endpoint);
    if(params.toString() !== ''){
      url = endpoint + '?' + params;
    }
    return this.authFetch(url, {}, refreshToken)
      .then(res => {
        status = res.status;
        return res;
      })
      .then(res => new Response(res, status));
  }
}

export default new IslandHttpClient();
