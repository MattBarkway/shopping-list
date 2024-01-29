import type { PageServerLoad } from './$types';
import { addItem, getItems, getList } from '$lib/server/api';
import { type Actions, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, cookies }) => {
	const token = cookies.get('token');
	if (!token) {
		return;
	}
	const response = await getList(token, params.listID);
	const itemResponse = await getItems(token, params.listID);
	const items = await itemResponse.json()
	console.log({items});
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return {
		list: await response.json(),
		items: await items,
	};
};

export const actions = {
	default: async ({ params, cookies, request }) => {
		const data = await request.formData();
		const item = data.get('item');
		const token = cookies.get('token');
		if (!params.listID) {
			redirect(302, '/');
		}

		if (item && token) {
			const response = await addItem(token, params.listID, {
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
