import { useRouter } from 'next/navigation';
import { useRegistrationStatusQuery } from '@/redux/features/api/authentication/authenticationEndpoints';
import { useEffect } from 'react';
import { PATHS } from '@/constants/paths.constants';

const useRedirectToRegistration = () => {
    const router = useRouter();
    const { data: registrationStatus, isLoading: isRegistrationStatusLoading } =
        useRegistrationStatusQuery(null);

    useEffect(() => {
        if (
            !isRegistrationStatusLoading &&
            registrationStatus?.registrationNeeded
        ) {
            router.push(PATHS.REGISTRATION);
        }
    }, [isRegistrationStatusLoading, registrationStatus, router]);
};

export default useRedirectToRegistration;
