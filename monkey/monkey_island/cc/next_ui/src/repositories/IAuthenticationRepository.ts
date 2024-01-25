export type AuthenticationResult = {
    isError: boolean;
    error: any;
};

export default interface IAuthenticationRepository {
    login(username: string, password: string): Promise<AuthenticationResult>;
    register(username: string, password: string): Promise<AuthenticationResult>;
    logout(): Promise<AuthenticationResult>;
    // Perhaps a method to check if the user is logged in?
}

// ISP should separate the methods into different interfaces...
// A React hook to provide the authentication repository
// Actually, this can be done via a context provider
