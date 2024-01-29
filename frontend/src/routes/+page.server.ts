import type { PageServerLoad } from './$types';
import { getLists } from "$lib/server/api";

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('token')
	if (!token) {
		return;
	}
	const response = await getLists(token)
	if (response.status === 401) {
		return;
	}
	return {
		lists: await response.json(),
	};
};
