import type { Actions } from './$types';
import { createList, register } from '$lib/server/api';

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const name = data.get('name');
		let token = cookies.get('token');
		if (name && token) {
			let response = await createList(token, name.toString());
			if (response.ok) {
				return { success: true };
			} else if (response.status === 422) {
				let err = (await response.json())['detail'];
				console.log(err);
				return { error: err };
			} else {
				return { error: 'Seems like we might be having issues, please try again later.' };
			}
		}
	}
} satisfies Actions;
