import * as awilix from 'awilix';

// Import dependencies
import { store } from '@/redux/store';
import RTKAuthenticationRepository from '@/repositories/RTKAuthenticationRepository';
import buildAppAvatar from '@/components/app-nav/app-avatar/AppAvatar';
import buildAvatarMenu from '@/components/app-nav/app-avatar/avatar-menu/AvatarMenu';
import buildMonkeyAppBar from '@/components/app-nav/app-bar/AppBar';
import buildLogoutButton from '@/components/logout-button/LogoutButton';

export const container = awilix.createContainer({
    injectionMode: awilix.InjectionMode.CLASSIC,
    strict: true
});

container.register({
    store: awilix.asValue(store),
    authenticationRepository: awilix.asClass(RTKAuthenticationRepository),
    AppAvatar: awilix.asFunction(buildAppAvatar),
    AvatarMenu: awilix.asFunction(buildAvatarMenu),
    AppBar: awilix.asFunction(buildMonkeyAppBar),
    LogoutButton: awilix.asFunction(buildLogoutButton)
});

export default container;
