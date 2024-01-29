import type { PageServerLoad } from './$types';
import { getLists } from "$lib/server/api";
import { redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ cookies }) => {
	let token = cookies.get('token')
	if (!token) {
		return;
	}
	let response = await getLists(token)
	if (response.status === 401) {
		return;
	}
  return {
		lists: await response.json(),
	};
};
