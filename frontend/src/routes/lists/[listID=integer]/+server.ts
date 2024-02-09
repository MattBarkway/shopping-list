import type { RequestHandler } from './$types';
import { removeItem, updateItem } from "$lib/server/api";
import { redirect } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ params, cookies, request }) => {
	const token = cookies.get('token');
	if (!token) {
		return redirect(302, '/login');
	}
	const payload = await request.json();
	const response = await updateItem(token, params.listID, payload.id, {
		name: payload.name,
		description: '',
		quantity: payload.quantity
	});
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return new Response();
};

export const DELETE: RequestHandler = async ({ params, cookies, request }) => {
	const token = cookies.get('token');
	if (!token) {
		return redirect(302, '/login');
	}
	const payload = await request.json();
	const response = await removeItem(token, params.listID, payload.id);
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return new Response();
};
