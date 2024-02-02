import type { Actions } from './$types';
import { register } from "$lib/server/api";

export const actions = {
	default: async (event) => {
		const data = await event.request.formData();
		const username = data.get('email');
		const password = data.get('password');
		if (username && password) {
			let response = await register(username.toString(), password.toString());
			if (response.ok) {
				return { success: true };
			} else if (response.status === 422) {
				console.log()
				return { error: (await response.json())['detail'] };
			} else {
				return { error: 'Seems like we might be having issues, please try again later.' };
			}
		}}
} satisfies Actions;
