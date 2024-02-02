import type { PageServerLoad } from './$types';
import { validateCollaborator } from '$lib/server/api';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, cookies }) => {
	const token = cookies.get('token');
	if (!token) {
		// TODO can I add a token here?
		redirect(302, '/login');
	}
	const response = await validateCollaborator(token, params.listID, params.token);
	if (response.status === 401) {
		// TODO don't use path, use a global store/localstorage
		//list-id=${params.listID}&colab-token=${params.token}
		return redirect(302, '/login');
	} else if (response.status == 403) {
		return { error: 'Forbidden (are you signed in to the wrong account?)' };
	}
	return { success: true };
};
