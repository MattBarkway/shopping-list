export async function load({ fetch, params }) {
	console.log(params);
	const post = await getShoppingList(fetch, params.listID);

	if (post) {
		return { items: [1, 2, 3, 4] };
	}
	return { items: [1, 2, 3, 4] };

	// throw new Error('404, Not found');
}

async function getShoppingList(fetch, listID: number): Promise<any> {
	const response = await fetch(`http://localhost:8000/api/v1/shopping/${listID}`, {
		method: 'GET',
		headers: { Authorization: 'Bearer foo' }
	});
	if (response.status == 401) {
		console.log('not authorised, going to login');
	} else if (!response.ok) {
		// throw new Error('whoops');
	}
	return await response.json();
}
