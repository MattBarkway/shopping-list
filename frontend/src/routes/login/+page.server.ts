import type { Actions } from './$types';
import { login } from "$lib/server/api";
import { redirect } from "@sveltejs/kit";

export const actions = {
	default: async ({ cookies, request, params }) => {
		const data = await request.formData();
		const username = data.get('email');
		const password = data.get('password');
		if (username && password) {
			const response = await login(username.toString(), password.toString());
			if (response.ok) {
				const payload = await response.json();
				cookies.set('token', payload['access_token'], { path: '/', secure: true, sameSite: 'strict', maxAge: 60 * 60 * 24});
				return redirect(302, '/');
			} else if (response.status === 401) {
				return { error: 'Invalid credentials, please try again.'};
			} else if (response.status === 422) {
				return { error: (await response.json())['detail'] };
			} else {
				return { error: 'Seems like we might be having issues, please try again later.' };
			}
		}}
} satisfies Actions;
