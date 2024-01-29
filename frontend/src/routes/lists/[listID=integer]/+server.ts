import type { RequestHandler } from './$types';
import { updateItem } from "$lib/server/api";

export const POST: RequestHandler = async ({ request }) => {
	console.log('received request:', request)
	await updateItem(request.listID, request.itemID, request.item);
	return;
};
