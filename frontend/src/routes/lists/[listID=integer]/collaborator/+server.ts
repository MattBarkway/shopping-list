import type { RequestHandler } from './$types';
import { addCollaborator } from "$lib/server/api";
import { redirect } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ params, cookies, request }) => {
	const token = cookies.get('token');
	if (!token) {
		return redirect(302, '/login');
	}
	const payload = await request.json();
	const response = await addCollaborator(token, params.listID, payload.collaborator);
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return new Response();
};
