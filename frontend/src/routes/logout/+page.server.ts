import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	cookies.delete('token', {path: '/'});
	return {
		logged_out: true,
	}
};
