import type { RequestHandler } from './$types';
import { addCollaborator } from "$lib/server/api";
import { redirect } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ params, cookies, request }) => {
	console.log("we made it yay");
	const token = cookies.get('token');
	if (!token) {
		return redirect(302, '/login');
	}
	const payload = await request.json();
	console.log('received request:', payload);
	const response = await addCollaborator(token, params.listID, payload.collaborator);
	console.log(response.status)
	let gub = await response.json()
	console.log(gub);
	if (response.status === 401) {
		return redirect(302, '/login');
	}
	return new Response();
};
