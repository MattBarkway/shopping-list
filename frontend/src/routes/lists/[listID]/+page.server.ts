export async function load({ cookies }) {
	const auth = cookies.get('authToken');
  console.log({ auth });
  console.log(cookies.getAll());
	return auth;
}
