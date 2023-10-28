import { goto } from "$app/navigation";


export async function load(params: {listID: number}) {
	const post = await getShoppingList(params.listID);

	if (post) {
		return post;
	}

	throw new Error('404, Not found');
}

async function getShoppingList(listID: number): Promise<any> {
  const response = await fetch(`http://localhost:8000/api/v1/shopping/${listID}`);
  if (response.status == 401) {
    await goto('/login');
  } else if (!response.ok) {
    throw new Error('whoops');
  }
  return await response.json();
}
