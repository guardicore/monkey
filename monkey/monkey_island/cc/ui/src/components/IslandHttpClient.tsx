import AuthComponent from "./AuthComponent";
import React from "react";

export class Response{
  body: any
  status: number

  constructor(body: any, status: number) {
    this.body = body
    this.status = status
  }
}

class IslandHttpClient extends AuthComponent {
  post(endpoint: string, contents: any): Promise<Response>{
    return this.authFetch(endpoint,
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(contents)
      })
      .then(res => new Response(res.json(), res.status));
  }

  get(endpoint: string): Promise<Response>{
    return this.authFetch(endpoint)
      .then(res => new Response(res.json(), res.status));
  }
}

export default new IslandHttpClient();
