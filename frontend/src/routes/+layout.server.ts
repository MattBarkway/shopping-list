import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ cookies}) => {
	return {
		signed_in: !!cookies.get("token"),
	};
};