import type { Actions } from './$types';
import { createList } from '$lib/server/api';
import { redirect } from "@sveltejs/kit";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const name = data.get('name');
		const token = cookies.get('token');
		if (name && token) {
			const response = await createList(token, name.toString());
			if (response.ok) {
				const data = await response.json()
				return redirect(302, `/lists/${data.id}`)
			} else if (response.status === 422) {
				const err = (await response.json())['detail'];
				return { error: err };
			} else {
				return { error: 'Seems like we might be having issues, please try again later.' };
			}
		}
	}
} satisfies Actions;
