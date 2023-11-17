export async function getLists() {
  ''
  let lists = [
    {
      name: "Big shop",
      owner: "mdbarkway@gmail.com",
      shared_with: [],
      item_count: 23,
      last_updated: "yes",
      id: 1,
    },
    {
      name: "Quick shop",
      owner: "mdbarkway@gmail.com",
      shared_with: [],
      item_count: 3,
      last_updated: "yes",
      id: 2,
    },
  ]
  // let token = localStorage.getItem('authToken')
  //
  const response = await fetch('http://localhost:8000/api/v1/shopping/', {
		method: 'GET',
    headers: {
      Authorisation: `Bearer foo`,
    }
	});
  return lists;
}
