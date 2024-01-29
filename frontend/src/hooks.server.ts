// import type { Handle } from '@sveltejs/kit';
//
// export const handle: Handle = async ({ event, resolve }) => {
// 	event.locals.user = await getUserInformation(event.cookies.get('sessionid'));
//
// 	const response = await resolve(event);
// 	response.headers.set('x-custom-header', 'potato');
//
// 	return response;
// };
// Maybe redirect to /login if request unauthorised?
