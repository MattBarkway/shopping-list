import type { PageServerLoad } from './$types';
import { getLists } from '$lib/server/api';

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('token');
	if (!token) {
		return;
	}
	const response = await getLists(token);
	if (response.status === 401) {
		return;
	}
	const results = await response.json();
	return {
		lists: results.lists,
		sharedLists: results.shared_lists
	};
};
