import { useRouter } from 'next/navigation';
import { useRegistrationStatusQuery } from '@/redux/features/api/authentication/authenticationEndpoints';
import { useEffect } from 'react';
import { PATHS } from '@/constants/paths.constants';

const useRedirectToRegistration = () => {
    const router = useRouter();
    const { data: registrationStatus, isLoading: isRegistrationStatusLoading } =
        useRegistrationStatusQuery();

    useEffect(() => {
        if (
            !isRegistrationStatusLoading &&
            registrationStatus?.registrationNeeded
        ) {
            router.push(PATHS.SIGN_UP);
        }
    }, [isRegistrationStatusLoading, registrationStatus, router]);
};

export default useRedirectToRegistration;
