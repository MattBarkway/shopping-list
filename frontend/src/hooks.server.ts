import type { Handle } from '@sveltejs/kit';
import { getUser } from '$lib/server/api';
import { redirect } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname === '/login') {
		return await resolve(event);
	}
	const token = event.cookies.get('token');
	if (!token) {
		return redirect(302, '/login');
	}
	const response = await getUser(token);
	if (response.status == 200) {
		event.locals.user = await response.json();
		return await resolve(event);
	}
	return redirect(302, '/login');
};
