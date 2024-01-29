import type { PageServerLoad } from './$types';
import { addItem, getItems, getList } from '$lib/server/api';
import { type Actions, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, cookies }) => {
	let token = cookies.get('token');
	if (!token) {
		return;
	}
	let response = await getList(token, params.listID);
	let itemResponse = await getItems(token, params.listID);
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return {
		list: await response.json(),
		items: await itemResponse.json()
	};
};

export const actions = {
	default: async ({ params, cookies, request }) => {
		const data = await request.formData();
		const item = data.get('item');
		let token = cookies.get('token');
		if (!params.listID) {
			redirect(302, '/');
		}

		if (item && token) {
			let response = await addItem(token, params.listID, {
				name: item.toString(),
				quantity: 1,
				description: ''
			});
			if (response.ok) {
				return { success: true };
			} else if (response.status === 422) {
				console.log();
				return { error: (await response.json())['detail'] };
			} else {
				return { error: 'Seems like we might be having issues, please try again later.' };
			}
		}
	}
} satisfies Actions;
